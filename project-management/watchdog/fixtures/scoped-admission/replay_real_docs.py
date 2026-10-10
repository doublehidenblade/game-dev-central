"""Replay a real immutable docs packet inside SYNTHETIC scoped collection.

Inputs stay outside the repository. This test emits no dispatch/merge receipt,
performs no network requests, and does not refresh identities or timestamps.
The archived packet is byte/semantic pinned below. It is NOT current authority.
"""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import coordinator as co
import evidence_policy as ep


def run(snapshot, negative_authority, negative_objects):
    packet = snapshot["evidence_policy"]["td-218-docs-admission-board"]
    authority, submission = packet["authority"], packet["submission"]
    assert ep.digest(authority) == "a0f80b4a4c373603699651a6171d1f99e217cf2e48777f378ce56f9b3310e35f"
    assert ep.digest(submission) == "28710c7b3904b894a3a9739f5f874ff949c23f7ae53be6abb379aeebe883cc24"
    assert authority["candidate"]["implementation_head"] == "cd252d15a910065deb3c53129d9a6680feee94e2"
    assert authority["candidate"]["artifact_head"] == "0abe43e01f4186f5ce480aba9c0bd32ae105cb6e"
    assert all("SYNTHETIC" in r["provenance"] for r in snapshot["scoped_source"]["receipts"])
    assert all("SYNTHETIC" in r["evidence"] for r in snapshot["requests"])
    at = ep.utc(snapshot["observed_at"])
    proof = ep.evaluate_completion(authority, submission, packet["objects"], at)
    result = co.evaluate(snapshot, at)
    assert proof["status"] == "ACCEPTABLE", proof
    assert result["status"] == "ACTION_REQUIRED" and len(result["actions"]) == 1, result
    assert result["source_scope"]["global_coverage"] == "unknown"
    # The only declared check is an actual call of the unchanged policy above.
    assert snapshot["tasks"][0]["required_checks"] == ["evidence-policy:acceptance-check"]
    negative = ep.evaluate_completion(negative_authority, submission, negative_objects,
                                      ep.utc(negative_authority["observed_at"]))
    assert negative["status"] == "NO_GO" and any(i["code"] == "STALE_ACKNOWLEDGMENT" for i in negative["issues"]), negative
    return {"control": "real immutable documentation packet with synthetic surrounding scoped collection",
            "historical_evidence_policy": proof["status"],
            "historical_scoped_algorithm": result["status"],
            "global_coverage": result["source_scope"]["global_coverage"],
            "current_rule_negative": negative["status"],
            "negative_codes": [i["code"] for i in negative["issues"]],
            "snapshot_sha256": ep.digest(snapshot),
            "authority_sha256": ep.digest(authority), "submission_sha256": ep.digest(submission),
            "limitations": ["Historical replay is not current eligibility", "Collection/ownership/queue/executor receipts are synthetic test controls",
                            "No private source observations are published", "No game, gameplay, visual, runtime, Actions or deployment check is inferred"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--negative-authority", required=True)
    parser.add_argument("--negative-objects", required=True)
    args = parser.parse_args()
    with open(args.snapshot, encoding="utf-8") as f:
        snapshot = json.load(f)
    with open(args.negative_authority, encoding="utf-8") as f:
        negative_authority = json.load(f)
    with open(args.negative_objects, encoding="utf-8") as f:
        negative_objects = json.load(f)
    print(json.dumps(run(snapshot, negative_authority, negative_objects), indent=2))
