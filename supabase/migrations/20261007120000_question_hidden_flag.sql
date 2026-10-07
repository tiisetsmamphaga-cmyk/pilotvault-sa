-- Hide a question from students without deleting it (for example a
-- duplicate of another question). Reversible: set is_hidden back to false.
alter table public.questions
  add column if not exists is_hidden boolean not null default false;

comment on column public.questions.is_hidden is
  'When true the question is not served to students (practice, mocks or trial).';
