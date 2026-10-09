-- Session activity for /admin (applied to production on 2026-10-09).
-- auth.sessions isn't exposed through the API, so the admin overview reads it
-- through this function: one row per user with a live session, and when that
-- session last did anything (sign-in or token refresh, which an open tab does
-- about hourly). Only the service role may call it.
create or replace function public.admin_session_activity()
returns table (user_id uuid, session_count integer, last_active_at timestamptz)
language sql
stable
security definer
set search_path = ''
as $$
  select
    s.user_id,
    count(*)::integer,
    max(greatest(s.created_at, s.updated_at, s.refreshed_at at time zone 'UTC'))
  from auth.sessions s
  where s.not_after is null or s.not_after > now()
  group by s.user_id
$$;

revoke all on function public.admin_session_activity() from public, anon, authenticated;
grant execute on function public.admin_session_activity() to service_role;
