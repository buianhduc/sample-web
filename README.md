# AI Contest Platform

A Streamlit-based contest environment for LLM and DS tasks.

## Run locally

1. Install dependencies:

```bash
python -m pip install -r requirements.md
```

2. Start the app:

```bash
streamlit run src/main.py
```

## Pages

- `Home`: overview and contest instructions.
- `LLM Task`: task instructions and sample submission bundle.
- `DS Task`: task instructions and sample submission bundle.
- `Submit Results`: login/register and upload result files.
- `Leaderboard`: ranking by task and score.
- `Submission History`: team history and previous results.

## Upload format

Required columns:

- `id`
- `function`
- `param`
- `time`

Supported upload types: `.csv`, `.xls`, `.xlsx`.

## Improvements

- Team authentication now uses hashed passwords.
- Session state preserves login across submission and history pages.
- Task page rendering is shared in `src/app_core.py`.
- Caching is enabled for task descriptions and answer keys.
