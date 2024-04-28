#! /usr/bin/env python3

"""Create a token block list for a given tokenizer.json file"""

import argparse
import json
import re

PATTERNS = {"no-chinese": r"[^\u4e00-\u9fff]"}


def bytes_to_unicode():
    bs = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    cs = bs[:]
    n = 0
    for b in range(2**8):
        if b not in bs:
            bs.append(b)
            cs.append(2**8 + n)
            n += 1
    cs = [chr(n) for n in cs]
    return dict(zip(cs, bs))


def text_to_unicode(text: str, decoder):
    try:
        return bytearray([decoder[c] for c in text]).decode("utf-8")
    except UnicodeDecodeError:
        return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Token Blocker")
    parser.add_argument("input", type=str, help="tokenizer.json file")
    parser.add_argument("out", type=str, help="Output file for blocked tokens")
    parser.add_argument("-r", "--regex", type=str, help="Regex pattern. If this pattern is matched, the token will be omited from the block list")
    parser.add_argument("-p", "--preset", choices=PATTERNS.keys(), help="Select a pattern from the presets")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        tokenizer = json.load(f)

    decoder = bytes_to_unicode()

    # Get the vocabulary dictionary
    vocab_dict = tokenizer["model"]["vocab"]

    if args.preset:
        args.regex = PATTERNS[args.preset]

    regex = re.compile(args.regex)

    # # Filter out non-Chinese characters
    chinese_token_ids = {
        token_id: text_to_unicode(token, decoder)
        for token, token_id in vocab_dict.items()
        if not regex.match(text_to_unicode(token, decoder))
    }

    with open(args.out, "w") as f:
        f.write(", ".join([str(token_id) for token_id in chinese_token_ids.keys()]))
