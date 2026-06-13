import json

def dedupe(input_file='cenos_data.json', output_file='cenos_data_cleaned.json'):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ {input_file} not found. Nothing to deduplicate.")
        return
    except json.JSONDecodeError:
        print(f"⚠️ {input_file} is not valid JSON. Cannot process.")
        return

    unique_entries = []
    seen = set()

    for entry in data:
        identifier = json.dumps(entry, sort_keys=True)
        if identifier not in seen:
            seen.add(identifier)
            unique_entries.append(entry)

    with open(output_file, 'w') as f:
        json.dump(unique_entries, f, indent=2)

    print(f"✅ Dedupe complete: {len(data)} → {len(unique_entries)} entries")
    print(f"💾 Saved to {output_file}")

if __name__ == "__main__":
    dedupe()

