import os
import re

files = [
    '00_MASTER_README.md',
    'docs/phase1_setup.md',
    'docs/phase5_backend.md'
]

for fpath in files:
    if not os.path.exists(fpath): continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove all lines matching old keys
    lines = content.split('\n')
    new_lines = []
    skip = False
    for line in lines:
        if 'Key 1: Reddit' in line or 'Key 2: YouTube' in line:
            skip = True
            continue
        if skip and line.startswith('###'):
            skip = False
        if skip:
            continue
            
        if 'Reddit API rejects credentials' in line: continue
        if 'YouTube API key works but quota is zero' in line: continue
        if "ModuleNotFoundError: No module named 'praw'" in line: continue
        if 'config.yaml has placeholder text still in it' in line: continue
        if 'YouTube API key missing in config.yaml' in line:
            line = line.replace('YouTube', 'Gemini')
        if 'reddit.com/prefs/apps' in line:
            line = '- **Setup needed:** None (using unauthenticated JSON endpoints)'
        if 'delete the YouTube API key' in line:
            line = line.replace('YouTube API key', 'Gemini API key')
            
        new_lines.append(line)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print(f"Cleaned {fpath}")
