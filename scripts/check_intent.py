# check_indent.py
with open('core/social_poster.py', 'r') as f:
    for i, line in enumerate(f, 1):
        if line.strip() and not line.startswith('#'):
            spaces = len(line) - len(line.lstrip())
            if spaces % 4 != 0:
                print(f"Line {i}: Bad indent ({spaces} spaces): {line.strip()[:50]}")