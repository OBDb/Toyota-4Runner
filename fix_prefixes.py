#!/usr/bin/env python3
"""
Replace TOYOTA_ prefixes with 4RUNNER_ prefixes in default.json
"""
import json

# Load default.json
with open('signalsets/v3/default.json', 'r') as f:
    data = json.load(f)

# Count replacements
replacement_count = 0

# Update all signal IDs
for cmd in data['commands']:
    for signal in cmd.get('signals', []):
        if 'id' in signal and signal['id'].startswith('TOYOTA_'):
            signal['id'] = signal['id'].replace('TOYOTA_', '4RUNNER_', 1)
            replacement_count += 1

print(f"Replaced {replacement_count} signal IDs from TOYOTA_ to 4RUNNER_")

# Save updated file
with open('signalsets/v3/default.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Saved updated default.json")
