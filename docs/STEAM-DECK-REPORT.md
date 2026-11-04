# Steam Deck tester: one-command privacy-safe report

From the repository's extracted root in Steam Deck Desktop Mode / Konsole, with the game running:

```bash
python3 scripts/linux/azs-compat-report.py
```

Copy the output to the maintainer. It contains counts, runtime hints, OS architecture and desktop session, but **no game paths, usernames, Steam app IDs or PIDs**. The report does not alter game processes or prove the speed hooks work.

The probe is intentionally conservative: a game running through Proton may not be detected from Linux argv. If the count is zero, do not infer the game is not running.

**Not a release package.** This is a developer diagnostic script until verified on a Steam Deck.
