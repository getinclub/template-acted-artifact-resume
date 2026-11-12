"""Immutable offline transport records. No network requests are made."""
from dataclasses import dataclass
import hashlib
@dataclass(frozen=True)
class Manifest:
    etag: str
    size: int
    sha256: str
@dataclass(frozen=True)
class Partial:
    etag: str
    data: bytes
@dataclass(frozen=True)
class Response:
    status: int
    etag: str
    content_range: str | None
    body: bytes
class TransferError(ValueError):
    pass
def manifest(data, etag):
    return Manifest(etag, len(data), hashlib.sha256(data).hexdigest())
