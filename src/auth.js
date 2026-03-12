// =============================================================
// PokeFinder — Auth helpers
// Requires: src/config.js loaded first (exposes `sb`)
// =============================================================

/** Return the current session, or null if not logged in. */
async function getSession() {
  const { data } = await sb.auth.getSession();
  return data.session;
}

/** Return the current user object, or null. */
async function getUser() {
  const session = await getSession();
  return session ? session.user : null;
}

/**
 * Sign in with email + password.
 * Returns { user, error }.
 */
async function signIn(email, password) {
  const { data, error } = await sb.auth.signInWithPassword({ email, password });
  return { user: data?.user ?? null, error };
}

/**
 * Sign up a new user.
 * role: 'collector' | 'seller'
 * meta: { display_name, ... }  — stored in profiles via DB trigger
 */
async function signUp(email, password, role = 'collector', meta = {}) {
  const { data, error } = await sb.auth.signUp({
    email,
    password,
    options: {
      data: { role, ...meta },
    },
  });
  return { user: data?.user ?? null, error };
}

/** Sign out the current user. */
async function signOut() {
  await sb.auth.signOut();
}

/**
 * Sign in / sign up with Google OAuth.
 * redirectTo: where Supabase redirects after the OAuth flow.
 */
async function signInWithGoogle(redirectTo = window.location.origin) {
  const { error } = await sb.auth.signInWithOAuth({
    provider: 'google',
    options: { redirectTo },
  });
  if (error) console.error('Google OAuth error:', error.message);
}

/**
 * Guard: redirect to loginUrl if the user is not logged in,
 * or does not have the required role.
 * role: 'collector' | 'seller' | null (any authenticated user)
 */
async function requireAuth(loginUrl = '../../index.html', role = null) {
  const session = await getSession();
  if (!session) {
    window.location.href = loginUrl;
    return null;
  }
  if (role) {
    const { data } = await sb
      .from('profiles')
      .select('role')
      .eq('id', session.user.id)
      .single();
    if (!data || data.role !== role) {
      window.location.href = loginUrl;
      return null;
    }
  }
  return session.user;
}

/**
 * Listen for auth state changes (sign‑in, sign‑out, token refresh).
 * callback: (event, session) => void
 */
function onAuthStateChange(callback) {
  sb.auth.onAuthStateChange(callback);
}
