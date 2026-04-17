-- ═══════════════════════════════════════════════════════════
-- Mahd (مهد) — Supabase Schema Setup
-- Run these in your Supabase SQL Editor
-- ═══════════════════════════════════════════════════════════

-- 1. profiles table
CREATE TABLE IF NOT EXISTS public.profiles (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID UNIQUE NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    mother_name      TEXT NOT NULL,
    baby_name        TEXT NOT NULL,
    phone            TEXT NOT NULL,
    emergency_phone  TEXT NOT NULL,
    created_at       TIMESTAMPTZ DEFAULT now()
);

-- RLS: users can only read/write their own profile
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Own profile only" ON public.profiles
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);


-- 2. alerts table (danger event log)
CREATE TABLE IF NOT EXISTS public.alerts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    baby_name   TEXT,
    status      TEXT,
    created_at  TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.alerts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Own alerts only" ON public.alerts
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);


-- ═══════════════════════════════════════════════════════════
-- NOTE: In Supabase Dashboard → Authentication → Providers
-- Enable "Phone" provider and configure your SMS gateway
-- (Twilio is the easiest free option for testing)
-- ═══════════════════════════════════════════════════════════
