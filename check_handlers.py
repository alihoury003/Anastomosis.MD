import re

lines = open('dashboard.html', encoding='utf-8').read().split('\n')

# bridge block
bs = next(i for i, l in enumerate(lines) if 'Object.assign(window' in l)
be = bs
while '});' not in lines[be]:
    be += 1
bridge = ' '.join(lines[bs:be + 1])
bridge_tokens = set(t for t in re.split(r'[{},\s:]+', bridge) if re.fullmatch(r'[A-Za-z_$][\w$]*', t))

# script blocks (classic vs module)
blocks, i = [], 0
while i < len(lines):
    m = re.search(r'<script([^>]*)>', lines[i])
    if m and 'src=' not in m.group(1):
        kind = 'module' if 'module' in m.group(1) else 'classic'
        j = i
        while j < len(lines) and '</script>' not in lines[j]:
            j += 1
        blocks.append((i, j, kind))
        i = j
    else:
        i += 1
classic = '\n'.join('\n'.join(lines[a + 1:b]) for (a, b, k) in blocks if k == 'classic')
module = '\n'.join('\n'.join(lines[a + 1:b]) for (a, b, k) in blocks if k == 'module')
classic_defs = set(re.findall(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(', classic)) | set(
    re.findall(r'\b(?:const|let)\s+([A-Za-z_$][\w$]*)\s*=', classic))
window_assigns = set(re.findall(r'window\.([A-Za-z_$][\w$]*)\s*=(?!=)', module))
module_defs = set(re.findall(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(', module)) | set(
    re.findall(r'\b(?:const|let)\s+([A-Za-z_$][\w$]*)\s*=', module))

handler_re = re.compile(r'\son\w+\s*=\s*["\']([A-Za-z_$][\w$]*)\s*\(')
handlers = {}
for ln, text in enumerate(lines, 1):
    for m in handler_re.finditer(text):
        handlers.setdefault(m.group(1), []).append(ln)

dead = []
for n, lns in sorted(handlers.items()):
    if n in bridge_tokens or n in classic_defs or n in window_assigns:
        continue
    dead.append((n, 'module-defined, unbridged' if n in module_defs else 'NOWHERE', lns))

print(f"inline handler names: {len(handlers)}")
for k in ['startBlockFromIds', 'startFreeTrial', 'showPaywall']:
    print(f"  {k}: {'bridge OK' if k in bridge_tokens else 'MISSING FROM BRIDGE'}")
print("dead handlers:", dead if dead else "NONE - all reachable")
print("old 'of 2 free blocks' copy remaining:", sum('of 2 free blocks' in l for l in lines))
print("lines referencing TRIAL_QUESTION_LIMIT:", sum('TRIAL_QUESTION_LIMIT' in l for l in lines))
print("upgrade pills:", sum('onclick="showPaywall()" style="background:var(--teal)' in l for l in lines))
print("first-day constant:", [l.strip() for l in lines if 'FIRST_DAY_QUESTIONS =' in l])
