#!/usr/bin/env python3
"""
Integrate non-EV parameters from toyota.json into default.json
"""
import json

# Load the filtered commands
with open('toyota_filtered.json', 'r') as f:
    filtered_data = json.load(f)

# Load default.json
with open('signalsets/v3/default.json', 'r') as f:
    default_data = json.load(f)

non_ev_commands = filtered_data['non_ev_commands']

print(f"Integrating {len(non_ev_commands)} commands into default.json")

# Process each command to convert debugfilter to dbg: true
for cmd in non_ev_commands:
    # Remove debugfilter if it exists and add dbg: true
    if 'debugfilter' in cmd:
        del cmd['debugfilter']
    cmd['dbg'] = True

    # Make sure we don't have both dbg and dbgfilter
    if 'dbgfilter' in cmd:
        del cmd['dbgfilter']

# Append to default.json commands
default_data['commands'].extend(non_ev_commands)

print(f"Total commands in new default.json: {len(default_data['commands'])}")

# Save the updated default.json
with open('signalsets/v3/default.json', 'w') as f:
    json.dump(default_data, f, indent=2)

print("Integration complete! Saved to default.json")
print("\nNow reformatting with cli.py...")
