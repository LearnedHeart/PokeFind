// =============================================================
// PokeFinder — Supabase client configuration
// Fill in YOUR_SUPABASE_URL and YOUR_SUPABASE_ANON_KEY below.
// Find them at: Supabase Dashboard → Project Settings → API
// =============================================================

const SUPABASE_URL     = 'https://zgnwvurkosyxvdlakwuf.supabase.co';       // e.g. https://abcxyz.supabase.co
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpnbnd2dXJrb3N5eHZkbGFrd3VmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMxNjIyMDMsImV4cCI6MjA4ODczODIwM30.-k8WfmlNOZmcafhu3Pw-2heiPSiTyAaweT47iKdChok'; // starts with "eyJ..."

// FastAPI backend base URL (change for production)
const API_BASE = 'http://localhost:8000';

// Initialise the Supabase JS client (loaded via CDN as window.supabase)
const { createClient } = supabase;
const sb = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
