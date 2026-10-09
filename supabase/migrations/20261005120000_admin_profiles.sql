-- Admin profiles (applied to production on 2026-10-05).
--
-- Admins are listed in public."Admins". A signed-in user can only see their
-- own row; there are no insert/update/delete policies, so the list can only be
-- changed with the service role (SQL editor or a migration).
--
-- The two admin accounts (thami@admin.com, tiisetso@admin.com) were created as
-- confirmed email/password users before this ran. To add another admin:
--   insert into public."Admins" (user_id)
--   select id from auth.users where email = '<email>';
-- and give their profile full access as in the update at the end of this file.

create table if not exists public."Admins" (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

alter table public."Admins" enable row level security;

create policy "Users can see their own admin row" on public."Admins"
  for select to authenticated
  using ((select auth.uid()) = user_id);

create or replace function public.is_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (select 1 from public."Admins" where user_id = auth.uid())
$$;

revoke all on function public.is_admin() from public, anon;
grant execute on function public.is_admin() to authenticated;

-- Admins can read every question, whatever their plan.
create policy "Admins can read all questions" on public.questions
  for select to authenticated
  using ((select public.is_admin()));

insert into public."Admins" (user_id)
select id from auth.users where email in ('thami@admin.com', 'tiisetso@admin.com')
on conflict (user_id) do nothing;

-- Admin profiles use the same "active PPL Pack" path as paying users, so every
-- subject and training mode unlocks without special cases in the app.
update public."Profiles" p
set subscription_status = 'active',
    subscription_plan = 'ppl',
    payment_status = 'admin',
    subscription_expires_at = '2099-12-31T23:59:59Z',
    trial_ends_at = null,
    updated_at = now()
where p.id in (select user_id from public."Admins");
