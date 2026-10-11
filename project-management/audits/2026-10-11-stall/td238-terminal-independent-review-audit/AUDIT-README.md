# td-238 independent review audit export

Export-only private delivery to Craig. All pre-existing evidence bytes are preserved unchanged. No Godot, runner, probe or product test was rerun. No GitHub mutation or publication was performed.

Verdict: CHANGES_REQUIRED. T1/T2/T4/T5 pass; T3 fails two focus restoration cases. Author correction budget remains exhausted (zero remaining). The original reports retain all acceptance limits.

Artifact head: 709ea8711799cd44a87db643eef7409ac16f8e44
Implementation head: fd8776c02aefab4f4de6cc0d2208838be93990d4

Start with td238-review-evidence/REVIEW.md and independent-review.json. AUDIT-INVENTORY.json lists every included file, exact byte count, SHA256, prior matching PR684 artifacts and publication status.

47 existing evidence files; 29 have unpublished review-specific bytes; 18 are byte-identical to evidence already in the reviewed PR artifact. None of these reviewer-local paths was uploaded to GitHub by this reviewer.

Unpublished review-specific files:

- td238-review-evidence/REVIEW.md
- td238-review-evidence/T1/T1-execution.json
- td238-review-evidence/T2/T2-execution.json
- td238-review-evidence/T3/T3-execution.json
- td238-review-evidence/T3/T3-raw.log
- td238-review-evidence/T4/T4-execution.json
- td238-review-evidence/T5/T5-execution.json
- td238-review-evidence/Xorg.98.log
- td238-review-evidence/adversarial/initial-probe-failure.txt
- td238-review-evidence/adversarial-rerun/T3-raw.log
- td238-review-evidence/adversarial-rerun/execution.json
- td238-review-evidence/adversarial-rerun/review-long-help-1280x720-bottom.png
- td238-review-evidence/adversarial-rerun/review-long-help-960x540-bottom.png
- td238-review-evidence/adversarial-rerun/review-unavailable-1280x720-bottom.png
- td238-review-evidence/adversarial-rerun/review-unavailable-960x540-bottom.png
- td238-review-evidence/evidence-files.json
- td238-review-evidence/execution-schema-check.json
- td238-review-evidence/final-state-and-triggers.json
- td238-review-evidence/focus-probe/T2-raw.log
- td238-review-evidence/focus-probe/execution.json
- td238-review-evidence/focus-probe-native/T3-raw.log
- td238-review-evidence/focus-probe-native/execution.json
- td238-review-evidence/focus-probe.txt
- td238-review-evidence/image-comparison.json
- td238-review-evidence/independent-probe-initial.txt
- td238-review-evidence/independent-probe.txt
- td238-review-evidence/independent-review.json
- td238-review-evidence/probe-reproduction.txt
- td238-review-evidence/source-equivalence.json

Excluded: native-cache/ (font caches) and library-helper/ (transfer utility). Original excluded files remain untouched. No original evidence was edited or deleted.

The audit inventory and this README are new export metadata, not new validation evidence or an acceptance attestation.
