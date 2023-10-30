import pathlib
import sys
import textwrap

name = sys.argv[1]
override_file = pathlib.Path('override.g4')
if override_file.exists():
    override = override_file.read_text()
    override_lead = override.split(' ', 1)[0]
else:
    override = ''
    override_lead = ''

print(f"grammar {name};")
print()

for line in sys.stdin:
    line = line[:-1]

    if override_lead.endswith(':') and line.startswith(override_lead):
        print(override, end="")
        break

    if line.startswith("?start: "):
        line = line[1:]

    for s1, s2 in [
        ('"i', '"'),
        ('"', "'"),
        ("/[", "["),
        (r"\/", "/"),
        ("]/", "]"),
    ]:
        line = line.replace(s1, s2)


    if line:
        line += ' ;'

    print(line)
