# Token Blocker (Oobabooga WebUI Extension)

This is a extension, which dynamically loads and applys token block lists specific to each model.

## Usage

1. Create a file with the same name as the model to which it should be applied and save it under [/block-lists](block-lists).
2. Start the WebUi with the extension activated (`--extensions token-blocker`)

The block list will be automatically applied, when a model with the same name is used for inference.

## create-blocklist.py

The `create-blocklist.py` script creates a blocklist for a specific tokenizer using regex patterns.

```bash
$ create-blocklist.py --help
usage: create-blocklist.py [-h] [-r REGEX] [-p {no-chinese}] input out

Token Blocker

positional arguments:
  input                 tokenizer.json file
  out                   Output file for blocked tokens

options:
  -h, --help            show this help message and exit
  -r REGEX, --regex REGEX
                        Regex pattern. If this pattern is matched, the token will be omited from the block list
  -p {no-chinese}, --preset {no-chinese}
                        Select a pattern from the presets
```

The script already includes the following presets:
- *no-chinese*: Creates a blocklist containing all tokens consisting only of chinese symbols