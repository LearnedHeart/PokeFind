-- =============================================================
-- PokeFinder — Supabase PostgreSQL Schema
-- Run this in: Supabase Dashboard → SQL Editor → New query → Run
-- =============================================================

-- ─── EXTENSIONS ──────────────────────────────────────────────
create extension if not exists "uuid-ossp";
create extension if not exists "unaccent";

-- Création d'une fonction unaccent "IMMUTABLE" pour contourner la restriction de PostgreSQL
create or replace function public.immutable_unaccent(text)
returns text
language sql
immutable strict
as $$
  select public.unaccent('unaccent', $1);
$$;

-- ─── ENUMS ───────────────────────────────────────────────────
create type user_role as enum ('collector', 'seller');
create type subscription_plan as enum ('free', 'premium', 'starter', 'pro');
create type product_type as enum ('etb', 'display', 'booster', 'coffret', 'tripack', 'blister', 'autre');
create type stock_action as enum ('entry', 'exit', 'correction');

-- ─── TABLE: profiles ─────────────────────────────────────────
-- One row per auth.users entry. Created automatically on signup via trigger.
create table public.profiles (
  id            uuid primary key references auth.users(id) on delete cascade,
  email         text not null,
  display_name  text,
  role          user_role not null default 'collector',
  subscription  subscription_plan not null default 'free',
  avatar_url    text,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- ─── TABLE: stores ───────────────────────────────────────────
create table public.stores (
  id            uuid primary key default uuid_generate_v4(),
  owner_id      uuid not null references public.profiles(id) on delete cascade,
  name          text not null,
  address       text,
  city          text,
  postal_code   text,
  lat           double precision,
  lng           double precision,
  phone         text,
  website       text,
  hours         jsonb,             -- {"lun":"9h-19h","mar":"9h-19h",...}
  is_online     boolean not null default false,
  subscription  subscription_plan not null default 'starter',
  is_active     boolean not null default true,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- ─── TABLE: products ─────────────────────────────────────────
create table public.products (
  id            uuid primary key default uuid_generate_v4(),
  name          text not null,
  series        text not null,
  type          product_type not null default 'autre',
  barcode       text unique,
  price_avg     numeric(8,2),
  image_url     text,
  description   text,
  language      text not null default 'FR',
  created_at    timestamptz not null default now(),
  -- Full-text search vector (French) corrigé
  fts           tsvector generated always as (
    to_tsvector('french'::regconfig, public.immutable_unaccent(coalesce(name,'') || ' ' || coalesce(series,'') || ' ' || coalesce(description,'')))
  ) stored
);

create index products_fts_idx on public.products using gin(fts);
create index products_barcode_idx on public.products(barcode);

-- ─── TABLE: stocks ───────────────────────────────────────────
create table public.stocks (
  id            uuid primary key default uuid_generate_v4(),
  store_id      uuid not null references public.stores(id) on delete cascade,
  product_id    uuid not null references public.products(id) on delete cascade,
  quantity      integer not null default 0 check (quantity >= 0),
  price         numeric(8,2),
  updated_at    timestamptz not null default now(),
  unique(store_id, product_id)
);

create index stocks_store_idx on public.stocks(store_id);
create index stocks_product_idx on public.stocks(product_id);

-- ─── TABLE: stock_events ─────────────────────────────────────
-- Audit log for every inventory change
create table public.stock_events (
  id            uuid primary key default uuid_generate_v4(),
  stock_id      uuid not null references public.stocks(id) on delete cascade,
  store_id      uuid not null references public.stores(id) on delete cascade,
  product_id    uuid not null references public.products(id) on delete cascade,
  action        stock_action not null,
  delta         integer not null,       -- positive=entry, negative=exit
  quantity_after integer not null,
  note          text,
  created_by    uuid references public.profiles(id),
  created_at    timestamptz not null default now()
);

create index stock_events_store_idx on public.stock_events(store_id);
create index stock_events_created_idx on public.stock_events(created_at desc);

-- ─── TABLE: search_events ────────────────────────────────────
-- Powers the trending algorithm
create table public.search_events (
  id            uuid primary key default uuid_generate_v4(),
  product_id    uuid references public.products(id) on delete cascade,
  query         text,
  user_id       uuid references public.profiles(id) on delete set null,
  created_at    timestamptz not null default now()
);

create index search_events_product_idx on public.search_events(product_id, created_at desc);

-- ─── TABLE: alert_subscriptions ──────────────────────────────
create table public.alert_subscriptions (
  id            uuid primary key default uuid_generate_v4(),
  user_id       uuid not null references public.profiles(id) on delete cascade,
  product_id    uuid not null references public.products(id) on delete cascade,
  radius_km     integer not null default 25,
  city          text,
  is_active     boolean not null default true,
  created_at    timestamptz not null default now(),
  unique(user_id, product_id)
);

-- ─── TABLE: alert_notifications ──────────────────────────────
create table public.alert_notifications (
  id            uuid primary key default uuid_generate_v4(),
  subscription_id uuid not null references public.alert_subscriptions(id) on delete cascade,
  store_id      uuid not null references public.stores(id) on delete cascade,
  product_id    uuid not null references public.products(id) on delete cascade,
  is_read       boolean not null default false,
  created_at    timestamptz not null default now()
);

create index alert_notif_user_idx on public.alert_notifications(subscription_id, is_read, created_at desc);

-- ─── VIEW: trending_products ─────────────────────────────────
create or replace view public.trending_products as
select
  p.*,
  count(se.id) filter (where se.created_at > now() - interval '24 hours') as search_count_24h,
  count(se.id) filter (where se.created_at > now() - interval '7 days')  as search_count_7d,
  (select count(*) from public.stocks s where s.product_id = p.id and s.quantity > 0) as store_count
from public.products p
left join public.search_events se on se.product_id = p.id
group by p.id
order by search_count_24h desc, search_count_7d desc;

-- ─── TRIGGER: auto-create profile on signup ──────────────────
create or replace function public.handle_new_user()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email, display_name, role, subscription)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'display_name', split_part(new.email, '@', 1)),
    coalesce((new.raw_user_meta_data->>'role')::user_role, 'collector'),
    'free'
  )
  on conflict (id) do nothing;
  return new;
exception when others then
  raise log 'handle_new_user error: %', sqlerrm;
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- ─── TRIGGER: update updated_at timestamps ───────────────────
create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_updated_at before update on public.profiles
  for each row execute procedure public.set_updated_at();

create trigger stores_updated_at before update on public.stores
  for each row execute procedure public.set_updated_at();

create trigger stocks_updated_at before update on public.stocks
  for each row execute procedure public.set_updated_at();

-- ─── ROW LEVEL SECURITY ──────────────────────────────────────
alter table public.profiles           enable row level security;
alter table public.stores             enable row level security;
alter table public.products           enable row level security;
alter table public.stocks             enable row level security;
alter table public.stock_events       enable row level security;
alter table public.search_events      enable row level security;
alter table public.alert_subscriptions enable row level security;
alter table public.alert_notifications enable row level security;

-- profiles: users can read all, edit only their own
create policy "profiles_select_all" on public.profiles for select using (true);
create policy "profiles_update_own" on public.profiles for update using (auth.uid() = id);

-- stores: public read of active stores; sellers manage their own
create policy "stores_select_active" on public.stores for select using (is_active = true);
create policy "stores_insert_own"    on public.stores for insert with check (auth.uid() = owner_id);
create policy "stores_update_own"    on public.stores for update using (auth.uid() = owner_id);
create policy "stores_delete_own"    on public.stores for delete using (auth.uid() = owner_id);

-- products: public read; any authenticated user can create/update (open catalogue)
create policy "products_select_all"  on public.products for select using (true);
create policy "products_insert_auth" on public.products for insert with check (auth.uid() is not null);

-- stocks: public read; store owners manage their own
create policy "stocks_select_all"   on public.stocks for select using (true);
create policy "stocks_insert_own"   on public.stocks for insert
  with check (auth.uid() = (select owner_id from public.stores where id = store_id));
create policy "stocks_update_own"   on public.stocks for update
  using (auth.uid() = (select owner_id from public.stores where id = store_id));
create policy "stocks_delete_own"   on public.stocks for delete
  using (auth.uid() = (select owner_id from public.stores where id = store_id));

-- stock_events: sellers see their own store events
create policy "stock_events_select_own" on public.stock_events for select
  using (auth.uid() = (select owner_id from public.stores where id = store_id));
create policy "stock_events_insert_own" on public.stock_events for insert
  with check (auth.uid() = (select owner_id from public.stores where id = store_id));

-- search_events: insert only (analytics)
create policy "search_events_insert" on public.search_events for insert with check (true);

-- alert_subscriptions: users manage their own
create policy "alerts_select_own"  on public.alert_subscriptions for select using (auth.uid() = user_id);
create policy "alerts_insert_own"  on public.alert_subscriptions for insert with check (auth.uid() = user_id);
create policy "alerts_update_own"  on public.alert_subscriptions for update using (auth.uid() = user_id);
create policy "alerts_delete_own"  on public.alert_subscriptions for delete using (auth.uid() = user_id);

-- alert_notifications: users read their own
create policy "alert_notif_select_own" on public.alert_notifications for select
  using (auth.uid() = (select user_id from public.alert_subscriptions where id = subscription_id));
create policy "alert_notif_update_own" on public.alert_notifications for update
  using (auth.uid() = (select user_id from public.alert_subscriptions where id = subscription_id));