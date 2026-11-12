# The Download That Joined Two Releases

An authored 40-minute incident exercise. No real customer incident, network, CDN, production artifact, credential or platform runtime is involved.

## Start
Python 3.12+, standard library only. Run `python monitor.py`, then `python -m unittest discover -s tests -v`.
The starter intentionally fails: it promotes `ABCD5678` as release B because it only checks the eight-byte length. The genuine B is `WXYZ5678`.
Repair only `consume_response` and `ready_to_promote` in `downloader.py`. Open your PR against `main` when hosted by the exercise operator. The ZIP itself is not a published repository.

## Contract
`Manifest` is a trusted, immutable target acquired out of band: exact strong ETag, nonnegative byte size and lowercase SHA256. Input model fields have declared types; malformed manifests except weak/unquoted ETags are outside this exercise. ETags are opaque, case-sensitive quoted ASCII tokens in this fixture subset. Partial bytes and their stored ETag travel together. Transport removes content encodings; multi-range and compressed representations are unsupported. Each Response is the complete received HTTP message body, not a streaming fragment. No caller-owned input may be mutated.

- Before a real request, use Range `bytes=<local size>-` and If-Range with the stored strong ETag only when it matches the trusted manifest. Otherwise discard the stale partial and request the trusted target afresh. Request construction is provided as protocol context, not a learner function.
- Every response must match the manifest's strong ETag. Reject unsupported statuses with TransferError. Never silently switch target manifests to match a server response.
- A 200 response replaces, never appends to, any partial. Require no Content-Range and a full body whose length equals manifest size. A changed local identity is safe to discard here.
- A 206 may append only to the same target identity. Parse exactly `bytes start-end/total` with canonical nonnegative decimal numbers. Require start == current length, start <= end < total, total == manifest size and body length == end-start+1. Reject unknown totals, gaps, overlaps, multipart ranges and duplicates. Short successful ranges are allowed and can be resumed again.
- A 416 is not completion proof. Accept only exact `bytes */<manifest size>`, an empty body, the same identity and an already complete digest-verified local partial. Otherwise reject.
- `ready_to_promote` returns true only for matching strong identity, exact full length AND matching SHA256. Consumption may produce a full corrupt body; it must never pass this promotion gate. Failures preserve the immutable previous partial; callers may restart explicitly.

## Incident response
Inspect alias changes, local validator and range headers. Pause rollout; retain the last independently verified artifact. A clean full re-download of the trusted B is safe for this fixture; resuming blindly or skipping checksum is not. Preserve suspect bytes for diagnosis, do not serve them. State that checksum integrity depends on a trusted manifest and is not publisher authentication. This package does not implement signatures, durable/atomic filesystem publication, retries, bandwidth limits or full RFC conformance.

## Evidence
Monitor demonstrates the changed-representation rejection and clean restart. Tests cover all three statuses, segmented progress, retries, headers, lengths, validators and corruption. Green unit tests prove this model only, not CDN correctness or hosted engine integration.
