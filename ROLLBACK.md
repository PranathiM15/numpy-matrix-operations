# Rollback guide

This project uses Git commits as known-good source snapshots. Use rollback if a future change breaks the site or causes a deployment health check to fail.

## Before the first deployment

After your local tests pass and the repository is pushed, mark the known-good baseline:

```powershell
git tag -a v1.0.0 -m "Known-good Matrix Studio baseline"
git push origin v1.0.0
git log --oneline --decorate -5
```

Take a screenshot of the passing unit tests and the GitHub tag/commit page. Keep those with the task submission as baseline evidence.

## Revert a broken code change safely

1. Inspect recent history and identify the bad commit:

   ```powershell
   git log --oneline --decorate -10
   ```

2. Revert the bad commit (replace the placeholder with the real commit hash):

   ```powershell
   git revert <bad-commit-hash>
   git push origin main
   ```

3. Wait for the connected host to redeploy. Run the unit tests locally and check the deployed `/health` endpoint returns JSON with `"status":"ok"`. Also test addition and matrix multiplication in the web UI.
4. Record actual details in `evidence/ROLLBACK_EVIDENCE_TEMPLATE.md`. Do not call a planned rollback a completed rollback.

## Hosting-platform rollback

If the newest deployment fails but the previous deployment is healthy, open the service's Deploys/History page and redeploy the last successful deployment if that option is available. Confirm the resulting status is live, then re-run the checks described above. The exact controls can change by host, so use the controls currently shown in your service dashboard.

## Evidence checklist

- [ ] Passing local unit-test output captured.
- [ ] Baseline commit hash/tag recorded.
- [ ] Failed change/failed deployment ID recorded (if a rollback is needed).
- [ ] Rollback commit or redeployed deployment ID recorded.
- [ ] `/health` and UI smoke checks passed after rollback.
- [ ] Screenshot(s) and timestamps attached to the final submission.
