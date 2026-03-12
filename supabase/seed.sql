-- =============================================================
-- PokeFinder — Seed Data
-- Run AFTER schema.sql in: Supabase Dashboard → SQL Editor → New query → Run
-- =============================================================

-- ─── PRODUCTS ────────────────────────────────────────────────
insert into public.products (id, name, series, type, barcode, price_avg, image_url, language) values
  ('11111111-0001-0000-0000-000000000000', 'Coffret Dresseur d''Élite — Scarlet & Violet', 'Écarlate et Violet', 'etb',      '0820650854378', 59.99,  'https://assets.pokemon.com/assets/cms2/img/cards/web/SVI/SVI_EN_86.png', 'FR'),
  ('11111111-0002-0000-0000-000000000000', 'Booster Flammes Obsidiennes',                  'Flammes Obsidiennes', 'booster', '0820650854545', 5.49,   null, 'FR'),
  ('11111111-0003-0000-0000-000000000000', 'Display 36 boosters — Évolutions Prismatiques', 'Évolutions Prismatiques', 'display', '0820650121430', 169.99, null, 'FR'),
  ('11111111-0004-0000-0000-000000000000', 'Coffret Premier de Cordée — Lucario ex',        'Scarlet & Violet Base', 'coffret',  '0820650854408', 29.99,  null, 'FR'),
  ('11111111-0005-0000-0000-000000000000', 'Tripack Évolutions Prismatiques',               'Évolutions Prismatiques', 'tripack', '0820650121447', 14.99, null, 'FR'),
  ('11111111-0006-0000-0000-000000000000', 'Coffret Dresseur d''Élite — Paradox Rift',      'Paradox Rift', 'etb',             '0820650854552', 54.99,  null, 'FR'),
  ('11111111-0007-0000-0000-000000000000', 'Booster Masques de Crépuscule',                 'Masques de Crépuscule', 'booster', '0820650854613', 5.49,   null, 'FR'),
  ('11111111-0008-0000-0000-000000000000', 'Display 36 boosters — Masques de Crépuscule',  'Masques de Crépuscule', 'display', '0820650854620', 154.99, null, 'FR'),
  ('11111111-0009-0000-0000-000000000000', 'Coffret Collection Charizard ex',               'Obsidian Flames', 'coffret',      '0820650854484', 39.99,  null, 'FR'),
  ('11111111-0010-0000-0000-000000000000', 'Blister 3 boosters — Pokémon 151',              'Pokémon 151', 'blister',         '0820650121454', 19.99,  null, 'FR'),
  ('11111111-0011-0000-0000-000000000000', 'Display 36 boosters — Pokémon 151',             'Pokémon 151', 'display',         '0820650121461', 159.99, null, 'FR'),
  ('11111111-0012-0000-0000-000000000000', 'Coffret Dresseur d''Élite — Temporal Forces',   'Temporal Forces', 'etb',          '0820650854682', 54.99,  null, 'FR'),
  ('11111111-0013-0000-0000-000000000000', 'Booster Destins de Paldea',                     'Destins de Paldea', 'booster',  '0820650854699', 5.49,   null, 'FR'),
  ('11111111-0014-0000-0000-000000000000', 'Display 36 boosters — Flammes Obsidiennes',     'Flammes Obsidiennes', 'display', '0820650854521', 159.99, null, 'FR'),
  ('11111111-0015-0000-0000-000000000000', 'Coffret Ultra Premium — Charizard',             'Scarlet & Violet Base', 'coffret', '0820650854415', 119.99, null, 'FR');

-- ─── SEARCH EVENTS (simulate trending) ───────────────────────
-- Simulate searches during the last 24h so trending_products returns results.
insert into public.search_events (product_id, query, created_at)
select
  p.id,
  p.name,
  now() - (random() * interval '20 hours')
from public.products p,
     generate_series(1, 8) gs   -- 8 search events per product
where p.name like '%Évolutions Prismatiques%' or p.name like '%Charizard%' or p.name like '%151%';

insert into public.search_events (product_id, query, created_at)
select
  p.id,
  p.name,
  now() - (random() * interval '6 days')
from public.products p,
     generate_series(1, 3) gs
where p.name like '%Flammes%' or p.name like '%Masques%';