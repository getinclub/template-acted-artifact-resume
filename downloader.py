"""Repair these two functions; see README for the defined HTTP subset."""
from model import Partial, Response, Manifest, TransferError

def consume_response(partial: Partial, response: Response, target: Manifest) -> Partial:
    # BUG: blindly trusts byte count and appends any resumed body.
    if response.status in (200, 206):
        return Partial(response.etag, partial.data + response.body)
    if response.status == 416:
        return partial
    raise TransferError("unexpected response")

def ready_to_promote(partial: Partial, target: Manifest) -> bool:
    # BUG: a complete length is not proof of representation identity or integrity.
    return len(partial.data) == target.size
