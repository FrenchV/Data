# Gaze and joint attention

Course presentation by Saad Arshad, October 19, 2026.

## Study

Lorenzoni, A., & Dalmaso, M. (2026). Investigating the reversed congruency effect of gaze through the lens of joint attention. *Consciousness and Cognition, 143*, Article 104101. https://doi.org/10.1016/j.concog.2026.104101

Original data and analysis code: https://osf.io/h9f4v/ (Experiment 1).

## Course data

`gaze_exp1_trials.csv` is an analysis subset of the authors' `Results_Exp1.csv`. It contains 15,360 experimental trials from 60 participants. Practice/test records and the two test participant codes excluded by the authors' R script have been removed. Participant labels have been replaced with P001-P060. Recruitment identifiers, timestamps, device metadata, and demographics are omitted. No mapping back to the original identifiers is included.

Columns: `participant`, `stimulus` (Arrows/Gaze), `fixation` (Cross/Object), `congruency` (Congruent/Incongruent), `correct` (1/0), `rt_ms` (milliseconds, missing values allowed).

For reaction-time summaries, retain correct trials with 200 < RT < 1300 ms. This leaves 14,603 trials. First average within each participant and experimental cell, then calculate means and SDs across 60 participants. This gives each participant equal weight. These descriptive values differ slightly from trial-weighted means in the article and the earlier draft slides.

## Reproduction

Run `python analyse_gaze.py` (requires pandas) beside `gaze_exp1_trials.csv`. It creates `gaze_summary.csv`, `gaze_participant_means.csv`, `gaze_table.csv`, and `summary.json`. The included `build_gaze.mjs` creates the editable presentation figure and table from the JSON with `@oai/artifact-tool`.

The presentation reports the article's three-way interaction, b = -3.40 ms, p = .60, as a published result. The descriptive script does not refit the authors' Gamma mixed model.

The article is CC BY 4.0. Credit for the original research, data, and experiment belongs to Anna Lorenzoni and Mario Dalmaso. The analysis subset and presentation are course-project adaptations. Please consult the original OSF deposit for source files and their terms.
