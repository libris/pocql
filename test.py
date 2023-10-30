import json
import sys

import pocqlparser
from getexamples import getexamples

if __name__ == '__main__':
    args = sys.argv[1:]

    qs = getexamples()

    print("Test run")
    for q in qs:
        print(q)
        ast = pocqlparser.parse(q)
        print(json.dumps(ast, indent=2))
