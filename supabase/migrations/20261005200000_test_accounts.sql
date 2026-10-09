-- Test-account flag (applied to production on 2026-10-05).
-- Admins toggle it from /admin; flagged accounts are left out of every total,
-- the funnel, the charts and the trials-ending list. Students cannot change it
-- (Profiles has no update policy for authenticated users).
alter table public."Profiles" add column if not exists is_test_account boolean not null default false;
