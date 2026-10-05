# PilotVault UI standard

The reference design is the mock exam set-up pop-up
(`MockSetupDialog` in `app/practice/[subject]/components/training-mode-menu.tsx`).
New and reworked screens, dialogs and panels should follow it.

## Principles

- **Only what the student needs to decide or act.** Every word and icon must
  earn its place. If the control already says it, don't repeat it in a note.
- **No decorative icons.** Keep icons only where they act or carry meaning on
  their own: close (✕), show/hide password, back arrow. No icons beside
  headings, inside option cards, on list items or on primary buttons.
- **Short labels.** One or two words for headings and options ("Timer",
  "Show answers", "25 min", "Untimed", "On", "Off"). No descriptions under
  options; no summary lines that repeat the selection.
- **One line of rules, at most.** Only rules that change the outcome
  (e.g. "Pass mark 75%. Unanswered questions count as wrong.").
- **One primary action**, full width, plain text ("Start exam"). Secondary
  actions only when needed (e.g. "Continue" on an unfinished attempt).

## Dialogs

- Phones: bottom sheet (`items-end`, `rounded-t-3xl`), primary button pinned
  in a footer with `env(safe-area-inset-bottom)` padding; body scrolls.
- Larger screens: centred, `max-w-md`, `rounded-3xl`.
- Header: small uppercase context line (e.g. subject name) + short title, ✕ on
  the right. Close on ✕, Escape and backdrop click.
- Backdrop `bg-slate-950/60` with a light blur.

## Controls

- Choices are **segmented controls**: `bg-slate-100` track, `rounded-2xl`,
  `p-1`; options `h-11`, bold; selected option is a white pill with a soft
  shadow, others `text-slate-500`. Use `role="radiogroup"` / `role="radio"`
  with `aria-checked`.
- Use the same control for every setting in a panel so they read as one set.
- Disabled (e.g. trial-locked) options stay visible with a one-line note
  ("Fixed at 25 on the trial.").

## Colour and type

- Primary actions use the brand navy: `bg-[var(--pv-navy)]`, hover
  `bg-[var(--pv-navy-soft)]`. Note `app/brand-v2-navigation.css` remaps
  `#1f4e79` utility classes to navy outside the exam simulator, so use the
  variables directly in new code.
- Text: headings `text-slate-950`/`900` bold; secondary text `text-slate-500`,
  `text-xs`. Surfaces white with `border-slate-100` dividers and
  `bg-slate-50` for grouped cards.
- Must work at 390 px wide with a 20 px side gutter and no horizontal scroll.
