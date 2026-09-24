# ATG explanation rewrite

Record of the rewrite of all 356 Aircraft Technical & General explanations in the `questions` table.

- `original.json` - every ATG row (stem, options, correct answer, explanation) as it was before the rewrite.
- `pre-correction-4.json` - questions 2464, 2507, 2592 and 2616 as they were before their answers were
  corrected (their corrected state is what `original.json` holds).
- `scripts/atg_explanations/rewrites/*.py` - the new explanations, the filler options that were replaced,
  the two reworded stems (2426, 2638) and one typo fix to a correct answer (2665).
- `scripts/atg_explanations/apply.py` - validates the rewrites and generates the guarded SQL.

Every UPDATE was guarded on an md5 of the row's previous stem, options, answer and explanation, so it could
only apply to an unchanged row. To confirm the table still matches this record:

    python3 scripts/atg_explanations/apply.py --verify

and run the query it prints against the database; the two hashes must be equal. To revert a question, restore
its fields from `original.json` (or `pre-correction-4.json`).
