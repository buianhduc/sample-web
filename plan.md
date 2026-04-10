## Plan: Build Streamlit AI Contest Platform

TL;DR: Replace the starter Streamlit demo with a contest website using Streamlit and SQLite. Add `constants.py` and a DB layer, implement multipage contest flow for two tasks, user login/upload submission/results evaluation, and leaderboard persistence.

**Steps**
1. Review and clean the existing Streamlit starter app in `src/main.py`.
2. Create `src/constants.py` with contest constants only: page labels, task IDs, DB filename, upload config, scoring constants, expected upload columns, and allowed file extensions.
3. Create `src/db.py` to manage SQLite persistence:
   - initialize database and create tables for teams, submissions, tasks, and leaderboard history
   - register/validate team credentials
   - record submission metadata and evaluation results
   - query leaderboard and score history
4. Design the Streamlit app flow in `src/main.py` or via `src/pages/`:
   - Home page with contest overview and task selection
   - Problem page for LLM and DS tasks showing markdown description plus zip download link
   - Result submission page with username/password form and Excel upload handling
   - Score history page and task-specific leaderboard page
5. Add evaluation logic for uploaded Excel files:
   - require columns `id`, `function`, `param`, `time`
   - load the problem answer key from a resource file or test zip data
   - compare `function` and `param` for exact correctness
   - compute accuracy as correct count / total count
   - compute total score per row using the penalty formula with constants from `constants.py`
6. Persist and display results:
   - save each validated submission in SQLite
   - show user score history, including timestamp, accuracy, score, and elapsed time
   - compute and render a leaderboard by task, ranking by score and accuracy
7. Update project structure with resource directories for contest assets if needed (e.g. `resources/llm/`, `resources/ds/`).
8. Verify by running the app locally and checking the created SQLite file.

**Verification**
1. Start the app with `streamlit run src/main.py` and confirm the contest pages load.
2. Create or register one test user, upload a formatted Excel submission, and verify the app evaluates it and stores it in SQLite.
3. Confirm `constants.py` is used by the app and that the DB file exists after a submission.
4. Check leaderboard and score history display correct ranking and score calculations.

**Decisions**
- Use Streamlit for the web UI because the project already includes Streamlit dependencies and starter app code.
- Store contest configuration and scoring constants in `src/constants.py` as requested.
- Use SQLite for persistence with a simple `src/db.py` helper module.
- Build the platform around result upload/evaluation rather than implementing the full LLM/agent training workflow inside the app.

**Further considerations**
1. We should confirm whether the contest should require actual user registration or if a simple username/password check is enough.
2. We should decide whether leaderboard ranking is based on latest submission only or best submission over time.
3. We should decide whether both task leaderboards appear separately or a single combined leaderboard.
