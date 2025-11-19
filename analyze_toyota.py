#!/usr/bin/env python3
"""
Analyze toyota.json and identify non-EV/HV battery parameters for integration into default.json
"""
import json
import re

# Load toyota.json
with open('signalsets/v3/toyota.json', 'r') as f:
    toyota_data = json.load(f)

# Load default.json
with open('signalsets/v3/default.json', 'r') as f:
    default_data = json.load(f)

# Keywords that indicate EV/HV battery related parameters
# Be very specific - only exclude HV battery cells, modules, and SOC
EV_KEYWORDS = [
    'hvbat',           # High voltage battery
    'hv battery',      # High voltage battery spelled out
    'hv_bat',          # High voltage battery with underscore
    '_c01_v',          # Battery cell voltage patterns
    '_c02_v', '_c03_v', '_c04_v', '_c05_v', '_c06_v', '_c07_v', '_c08_v', '_c09_v',
    '_c10_v', '_c11_v', '_c12_v', '_c13_v', '_c14_v', '_c15_v', '_c16_v', '_c17_v',
    'cmu01', 'cmu02', 'cmu03', 'cmu04',  # Cell monitoring units
]

def is_ev_related(command):
    """Check if a command is EV/HV battery related"""
    # Check all signals in the command
    for signal in command.get('signals', []):
        signal_id = signal.get('id', '').lower()
        signal_name = signal.get('name', '').lower()
        signal_path = signal.get('path', '').lower()

        # Check if any EV keyword is in the signal
        for keyword in EV_KEYWORDS:
            if keyword in signal_id or keyword in signal_name:
                return True

    return False

# Filter non-EV commands
non_ev_commands = []
ev_commands = []

for cmd in toyota_data['commands']:
    if is_ev_related(cmd):
        ev_commands.append(cmd)
    else:
        non_ev_commands.append(cmd)

print(f"Total commands in toyota.json: {len(toyota_data['commands'])}")
print(f"EV/HV battery related commands: {len(ev_commands)}")
print(f"Non-EV commands to integrate: {len(non_ev_commands)}")
print()

# Show EV commands being excluded
print("=" * 80)
print("EV/HV BATTERY COMMANDS BEING EXCLUDED:")
print("=" * 80)
for cmd in ev_commands[:10]:  # Show first 10
    for signal in cmd['signals']:
        print(f"  - {signal['id']}: {signal['name']}")
if len(ev_commands) > 10:
    print(f"  ... and {len(ev_commands) - 10} more EV-related commands")
print()

# Show sample non-EV commands to integrate
print("=" * 80)
print("NON-EV COMMANDS TO INTEGRATE (Sample):")
print("=" * 80)
for cmd in non_ev_commands[:20]:  # Show first 20
    for signal in cmd['signals']:
        print(f"  - {signal['id']}: {signal['name']}")
if len(non_ev_commands) > 20:
    print(f"  ... and {len(non_ev_commands) - 20} more commands")
print()

# Save the filtered commands for review
output = {
    'non_ev_commands': non_ev_commands,
    'ev_commands': ev_commands
}

with open('toyota_filtered.json', 'w') as f:
    json.dump(output, f, indent=2)

print("Saved filtered commands to toyota_filtered.json for review")
