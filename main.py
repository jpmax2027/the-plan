#!/usr/bin/env python3
"""The Plan entry for make.fun.

Writes one short, concrete plan to /output/entry.txt: a plan an AI agent
can carry out itself, with a browser, code, APIs and $100, to turn $100
into the most money in 30 days.

Stdlib only, no network, deterministic output.
"""

import os
import tempfile

PLAN = (
    "Day 1: open a Fiverr gig writing SEO descriptions for Shopify "
    "sellers, $25 per 10 listings, with 5 free samples. Spend $20 on "
    "ads. Do 3-4 orders/day, reinvest profits, add a $50 store audit. "
    "Edge: agents sell generic writing; I own one niche with proof. "
    "$100 to $500+ in 30 days."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    text = PLAN
    # Gate: 1-280 Unicode code points, not only whitespace; ASCII only.
    encoded = text.encode("utf-8")
    if not (1 <= len(text) <= 280):
        raise SystemExit(f"plan length {len(text)} is outside 1-280 characters")
    if not text.strip():
        raise SystemExit("plan is only whitespace")
    if encoded.decode("utf-8") != text:
        raise SystemExit("plan is not valid UTF-8 round-trip")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(OUTPUT_PATH), prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(encoded)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, OUTPUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    # Verify what landed on disk matches exactly.
    written = open(OUTPUT_PATH, encoding="utf-8").read()
    if written != text:
        raise SystemExit("written entry does not match plan text")
    print(f"wrote {OUTPUT_PATH} ({len(text)} characters)")


if __name__ == "__main__":
    main()
