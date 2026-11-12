"""Synthetic byte replay, not a real HTTP server or deployed incident."""
import json
from model import Partial, Response, TransferError, manifest
from downloader import consume_response, ready_to_promote
A=b"ABCD1234"; B=b"WXYZ5678"; target=manifest(B, '"release-b"')
def run():
    old=Partial('"release-a"', A[:4])
    bad=Response(206, '"release-b"', 'bytes 4-7/8', B[4:])
    try:
        mixed=consume_response(old,bad,target)
        incident={"rejected":False,"bytes":mixed.data.decode(),"promotable":ready_to_promote(mixed,target)}
    except TransferError:
        incident={"rejected":True,"bytes":old.data.decode(),"promotable":False}
    fresh=consume_response(Partial('"release-b"',b""),Response(200,'"release-b"',None,B),target)
    return {"fixture":"authored offline replay", "changed_representation":incident,
            "clean_restart":{"bytes":fresh.data.decode(),"promotable":ready_to_promote(fresh,target)}}
if __name__=='__main__': print(json.dumps(run(),indent=2))
