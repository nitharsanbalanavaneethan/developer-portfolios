import re
import sys
from pathlib import Path

readme_path = Path(__file__).resolve().parents[1] / 'README.md'

errors = []
sections = {}
current_letter = None

with readme_path.open() as f:
    for idx, line in enumerate(f, start=1):
        line = line.rstrip('\n')
        m = re.match(r'^##\s+([A-Z])$', line)
        if m:
            current_letter = m.group(1)
            sections[current_letter] = []
            continue
        if line.startswith('- ['):
            m = re.match(r'- \[(.+?)\]\((.+?)\)', line)
            if not m:
                continue
            name, link = m.groups()
            if current_letter is None:
                errors.append(f'Entry outside section at line {idx}: {line}')
                continue
            sections[current_letter].append((name, link, idx))

# Check alphabetical order and duplicates
seen_names = {}
seen_links = {}
for letter, entries in sections.items():
    sorted_entries = sorted(entries, key=lambda x: x[0].lower())
    for i, entry in enumerate(entries):
        name, link, line_no = entry
        if entry != sorted_entries[i]:
            errors.append(f'Section {letter} not alphabetized at line {line_no}: {name}')
            break
        if name in seen_names:
            errors.append(f'Duplicate name "{name}" at line {line_no} (previous line {seen_names[name]})')
        else:
            seen_names[name] = line_no
        if link in seen_links:
            errors.append(f'Duplicate link {link} at line {line_no} (previous line {seen_links[link]})')
        else:
            seen_links[link] = line_no

if errors:
    for err in errors:
        print(err)
    sys.exit(1)
else:
    print('README validation passed.')
