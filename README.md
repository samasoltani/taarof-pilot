# Taarof Pilot

One-week pilot study: **ta'arof (تعارف) as action ascription** in one episode of the Persian TV show *Befarmaeed Sham*.

Research question: how do participants show whether they treat an offer or a refusal as genuine or ritual (e.g. explicit ascriptions such as «تعارف نکن»)?
Framework: Levinson (2013); Deppermann & Haugh (2022).

## Workflow

1. Claude pushes the next numbered script (`01-`, `02-`, ...).
2. Pull in PyCharm, run the script.
3. Each script writes its results to `outputs/` → commit & push.
4. Write e.g. "01 done" in the chat.

## Steps

| File | What it does | Output |
|---|---|---|
| `01-download_audio.py` | Downloads the episode audio (local only) | `outputs/01-download_info.txt` |

## Data policy

- Audio/video files stay on the local machine (`data/` is git-ignored) and are never shared.
- Only transcripts go into the repo; participant names will be replaced with pseudonyms.
- The repository is private.
