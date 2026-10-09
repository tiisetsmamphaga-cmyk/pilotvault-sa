-- Question reports (applied to production on 2026-10-05).
-- Students file a report with the Report button on a question; admins work
-- through them as tickets on /admin (read and updated with the service role).
create table if not exists public."QuestionReports" (
  id bigint generated always as identity primary key,
  question_id bigint not null references public.questions(id) on delete cascade,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  reason text not null check (reason in ('wrong_answer', 'question_error', 'explanation', 'diagram', 'other')),
  message text check (char_length(message) <= 1000),
  status text not null default 'open' check (status in ('open', 'resolved', 'dismissed')),
  admin_note text,
  created_at timestamptz not null default now(),
  resolved_at timestamptz,
  resolved_by uuid references auth.users(id) on delete set null
);

alter table public."QuestionReports" enable row level security;

-- Students may only file new, open reports as themselves; no read/update/delete.
create policy "Students can report questions" on public."QuestionReports"
  for insert to authenticated
  with check (
    (select auth.uid()) = user_id
    and status = 'open'
    and admin_note is null
    and resolved_at is null
    and resolved_by is null
  );

-- One open report per student per question.
create unique index if not exists question_reports_one_open_per_user
  on public."QuestionReports" (question_id, user_id) where status = 'open';
create index if not exists question_reports_status_created
  on public."QuestionReports" (status, created_at desc);

revoke all on public."QuestionReports" from anon;
