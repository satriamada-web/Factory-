# FACTORY — Automated Video Production

FACTORY is a phone-friendly, GitHub-based workflow for producing Indonesian faceless long-form fact videos.

## Project decisions

- Input: user-provided title and script, submitted in ChatGPT or as TXT/DOCX.
- Language: Indonesian.
- Topic: facts.
- Format: long-form video.
- Target: one video per day, subject to GitHub Actions quotas and successful quality tests.
- Script policy: preserve the user's title and script; do not generate or rewrite them with AI.
- Review policy: generated videos must be reviewed by the user before public release.
- Initial output: downloadable GitHub Actions artifact.
- Later integration: upload to YouTube as Private, after the rendering pipeline is tested.

## Planned pipeline

1. Validate and package the user-provided script.
2. Generate narration with an open-source TTS engine, subject to Indonesian voice availability and license checks.
3. Retrieve appropriately licensed visuals and retain attribution metadata.
4. Render video with FFmpeg.
5. Upload the rendered file as a GitHub Actions artifact.
6. Add YouTube Private upload only after the production pipeline is stable.

## Constraints

- Operated from Android through ChatGPT and GitHub.
- No VPS and no Termux.
- Prefer free and open-source components.
- GitHub Actions is quota-limited; this project does not assume unlimited or 24/7 compute.
- Never commit API keys, OAuth tokens, passwords, or other secrets.

## Current status

Repository selected. Initial implementation and end-to-end testing are pending.

