from pathlib import Path
from textwrap import dedent

INDENT = '    '


def getexamples():
    with (Path(__file__).parent / 'README.md').open() as f:
        return collectexamples(f)


def collectexamples(lines):
    examples = []
    current = []
    inexamples = False
    for line in lines:
        if line.strip() == '## Examples':
            inexamples = True
            continue
        if line.startswith('## '):
            inexamples = False
            continue

        if not inexamples:
            continue

        if line.startswith(INDENT):
            current.append(line)
        elif line.strip() and current:
            examples.append(dedent(''.join(current)))
            current = []

    if current:
        examples.append(''.join(current))

    return examples


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    x = int(args[0]) if args else -1
    for i, example in enumerate(getexamples()):
        if x == -1 or i == x:
            print(example)
