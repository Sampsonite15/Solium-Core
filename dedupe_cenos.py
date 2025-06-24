import json

# Load your JSON data
with open('cenos_data.json', 'r') as f:
    data = json.load(f)

# Remove duplicates
unique_entries = []
seen = set()

for entry in data:
    identifier = json.dumps(entry, sort_keys=True)  # convert to string for hashing
    if identifier not in seen:
        seen.add(identifier)
        unique_entries.append(entry)

# Save cleaned data
with open('cenos_data_cleaned.json', 'w') as f:
    json.dump(unique_entries, f, indent=2)

print(f"Original: {len(data)} entries → Unique: {len(unique_entries)} entries")