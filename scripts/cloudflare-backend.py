#!/usr/bin/env python3
# Requirements: pip install cryptography

import argparse
import hashlib
import json
import sys
import urllib.request

ENDPOINT = "https://autosave.worker.mon.icu"
USER_AGENT = "Mozilla/5.0 (MonikaAfterStory/recovery)"


def derive_user_id(uuid):
    return hashlib.sha512(uuid.encode("utf-8")).hexdigest()


def derive_key(uuid):
    return hashlib.pbkdf2_hmac("sha256", uuid.encode("utf-8"), b"fom-autosave-v1", 100000, 32)


def decrypt(data, key):
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        sys.exit("error: pip install cryptography")

    iv             = data[:12]
    tag            = data[12:28]
    ciphertext     = data[28:]
    return AESGCM(key).decrypt(iv, ciphertext + tag, None)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def cmd_list(uuid):
    user_id  = derive_user_id(uuid)
    versions = json.loads(fetch("{}/saves/{}/versions".format(ENDPOINT, user_id)))
    if not versions:
        print("No saves found.")
        return

    for v in versions:
        ts     = v["timestamp"][:19].replace("T", " ")
        kb     = v["size"] / 1024
        reason = v.get("reason", "autosave")
        print("{}  {}  {:.1f} KB  {}".format(v["sha256"], ts, kb, reason))


def cmd_get(uuid, sha256, output):
    user_id   = derive_user_id(uuid)
    key       = derive_key(uuid)
    encrypted = fetch("{}/saves/{}/{}".format(ENDPOINT, user_id, sha256))
    plaintext = decrypt(encrypted, key)

    if output:
        with open(output, "wb") as f:
            f.write(plaintext)
        print("Saved to {}".format(output))
    else:
        sys.stdout.buffer.write(plaintext)


def main():
    parser = argparse.ArgumentParser(description="mas-autosave cloud backend CLI")
    parser.add_argument("--uuid", required=True, metavar="UUID", help="backup code")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list saved versions")

    get_p = sub.add_parser("get", help="download and decrypt a save")
    get_p.add_argument("hash", help="SHA-256 hash from 'list'")
    get_p.add_argument("-o", "--output", metavar="FILE", help="write to file instead of stdout")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args.uuid)
    elif args.command == "get":
        cmd_get(args.uuid, args.hash, getattr(args, "output", None))


if __name__ == "__main__":
    main()
