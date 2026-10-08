# td-186 Tripo paid rig recovery — blocked retrieval

> Researched: 2026-10-07 by Codex, on Craig's asset-salvage request.

**Status: job IDs recovered; paid FBX still missing.** Preserve these identifiers so the existing result can be retrieved without paying for another rig. This note does not mark Asset Forge or visual/game acceptance complete.

## Asset and source

Target: suited-worker pedestrian's Mixamo-spec biped rigged character, intended as
`godot/assets/td-186/peds/mixamo/tripo_suited_worker_character.fbx`.

Implementation reference: [Tokyo Drift 3D PR #416](https://github.com/doublehidenblade/tokyo-drift-3d/pull/416), examined at `5cc19cb1cf906b84d9770b897d8719f53e2c0e2d`.
[Task td-186](https://github.com/doublehidenblade/tokyo-drift-3d/blob/5cc19cb1cf906b84d9770b897d8719f53e2c0e2d/godot/docs/tasks/td-186.md) reports one successful import/rig consuming 25 credits, followed by output-host denial.

The [rig script](https://github.com/doublehidenblade/tokyo-drift-3d/blob/5cc19cb1cf906b84d9770b897d8719f53e2c0e2d/godot/assets/td-186/source/tripo_rig.py) describes the input as `suited_worker` body and gear in rest A-pose, with no armature or ink shell, exported to `godot/assets/td-186/_scratch/tripo_input_suited_worker.glb`; rig settings are `biped`, `mixamo`, `fbx`. **The actual uploaded bytes/hash and exact original input chain still require provider metadata confirmation.**

## Recovered existing jobs

Source: Craig's authenticated official Tripo History export, recovered by the parent investigator and supplied to this recovery session. The export reports the same client ID across these successful records:

| Stage | Existing task ID | History status | Credits |
| --- | --- | --- | --- |
| Import | `1e0c5f36-93f2-4b70-8c38-fa9f8f35b565` | success | 0 |
| Pre-rig check | `7fe4340a-4cbf-4dd3-8bf0-43f9f8c5d0d6` | success | 0 |
| Paid rig | `471cddd5-39b1-4d03-a5f7-d2f4f52e3000` | success | 25 |

History time range: **2026-10-07 05:12:27–05:12:43; timezone unlabeled**. Do not interpret these timestamps as UTC without confirmation. No existing animation-retarget result has been established.

## Exact retrieval blocker

On **2026-10-07 at 13:04:10 UTC**, one authenticated GET for the existing rig at the documented v2 task endpoint on **`api.tripo3d.ai`** returned:

- HTTP **403**; Cloudflare **1010**.
- Error name: `browser_signature_banned`; category: `access_denied`.
- Detail: “The site owner has blocked access based on your browser's signature.”
- Response flags: `retryable=false`, `owner_action_required=true`; instruction: **Do not retry**.

No task metadata or output URL was returned. This does **not** mean the job is missing or the key is wrong; the creating-key match remains unverified. No further provider requests were made after this explicit denial. No signature, endpoint, proxy, environment, credential, network-policy, or allowlist workaround was attempted.

Separately, the original Claude run recorded denial at output host **`tripo-data.rg1.data.tripo3d.com`**. Its original HTTP status was not preserved in the examined repository evidence; this recovery session never reached an artifact request.

## Safe continuation, after permitted provider access is restored

1. Use the original creating credential and recovered rig ID to read existing task metadata through an authorized official path. Confirm the import/precheck/rig chain, input identity, type, time and credits before accepting an artifact.
2. Download only the existing result from the freshly returned official output URL, or use an already permitted authenticated official download UI. Do not evade an access denial.
3. Save the FBX and provenance, verify byte size and SHA256, inspect its FBX format and skeleton structurally, then hand it off for separate import/visual/game validation.

**Do not rerun `tripo_rig.py rig suited_worker`.** Missing records can cause new upload/import/rig jobs; even with a successful rig record, the command can submit a new paid `animate_retarget` job after download. The later ID-persistence patch cannot reconstruct the earlier lost log by itself.

Official documentation: [task query and creating-key requirement](https://docs.tripo3d.ai/task-query/get-your-task-result.html), [History availability](https://docs.tripo3d.ai/other/support-faq.html).

## Existing in-house asset remains intact

The committed [`ped_suited_worker.glb`](https://github.com/doublehidenblade/tokyo-drift-3d/blob/5cc19cb1cf906b84d9770b897d8719f53e2c0e2d/godot/assets/td-186/peds/ped_suited_worker.glb) is separate from the missing paid result. Direct structural inspection from the Git blob found GLB v2, **609,224 bytes**, matching declared length, **one skin / 23 joints**, and six clips: `cower`, `fall_death`, `hit_react`, `idle`, `run`, `walk`.

SHA256: `571b7995227b80f8be74169d644de3fbb7439a6ef45cf7172005cc9d82a2768d`.

No game asset or Claude implementation branch was changed. This recovery spent **zero additional credits**, submitted no jobs, performed no uploads, and made no account/security changes. No Actions were dispatched, merges performed, or deployments made. This document contains nonsecret job identifiers only: no credentials, tokens, signed download URLs, or raw provider responses.
