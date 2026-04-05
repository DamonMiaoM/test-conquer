"""
合并所有批次结果到 data/questions.json

数据来源:
1. 旧格式 JSON（完整批次）: batch_101-150_RESULT.json, batch_251-300_RESULT.json
2. 旧格式 JSONL: new_A1.json, new_A2.json, new_D1.json, new_D2.json, new_E1.json
3. 新格式 JSONL（本轮补全）: result_*.jsonl, batch_176-200_RESULT.json, batch_201-225_RESULT.json
"""

import json
import os

BATCHES_DIR = "/Users/Damon/Projects/Test Conquer/data/batches"
OUTPUT_FILE = "/Users/Damon/Projects/Test Conquer/data/questions.json"

def load_json(filepath):
    """Load a JSON array file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_jsonl(filepath):
    """Load a JSONL file (one JSON object per line)"""
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"  Warning: skipping invalid line in {filepath}: {e}")
    return records

def main():
    all_records = {}  # id -> record (dedup by latest)

    # Define all source files and their formats
    sources = [
        # Old intact JSON batches
        ("batch_101-150_RESULT.json", "json"),
        ("batch_251-300_RESULT.json", "json"),
        # Old JSONL files (partial data)
        ("new_A1.json", "jsonl"),
        ("new_A2.json", "jsonl"),
        ("new_D1.json", "jsonl"),
        ("new_D2.json", "jsonl"),
        ("new_E1.json", "jsonl"),
        # New round results (JSONL)
        ("result_16-25.jsonl", "jsonl"),
        ("result_31-50.jsonl", "jsonl"),
        ("result_51-75.jsonl", "jsonl"),
        ("result_76-100.jsonl", "jsonl"),
        ("result_161-175.jsonl", "jsonl"),
        ("result_189-200.jsonl", "jsonl"),
        ("result_221-240.jsonl", "jsonl"),
        ("result_241-250.jsonl", "jsonl"),
        # New round JSON results
        ("batch_176-200_RESULT.json", "json"),
        ("batch_201-225_RESULT.json", "json"),
    ]

    for fname, fmt in sources:
        filepath = os.path.join(BATCHES_DIR, fname)
        if not os.path.exists(filepath):
            print(f"  ⚠ Not found: {fname}")
            continue

        if fmt == "json":
            records = load_json(filepath)
        else:
            records = load_jsonl(filepath)

        count = 0
        for rec in records:
            if 'id' not in rec:
                continue
            qid = rec['id']
            # Later sources override earlier ones (newer data wins)
            all_records[qid] = rec
            count += 1
        print(f"  ✓ {fname}: {count} records loaded")

    # Sort by ID
    sorted_records = sorted(all_records.values(), key=lambda x: x['id'])

    # Validate: check for gaps
    all_ids = {r['id'] for r in sorted_records}
    expected = set(range(1, 301))
    missing = sorted(expected - all_ids)
    extra = sorted(all_ids - expected)

    print(f"\n{'='*50}")
    print(f"Total records: {len(sorted_records)}")
    print(f"Expected: 300 (IDs 1-300)")
    if missing:
        print(f"⚠ Missing IDs ({len(missing)}): {missing}")
    else:
        print(f"✅ All 300 questions present!")
    if extra:
        print(f"⚠ Extra IDs: {extra}")

    # Check field completeness
    incomplete = []
    for rec in sorted_records:
        if not rec.get('explanation') or not rec.get('source') or not rec['source'].get('url'):
            incomplete.append(rec['id'])
    if incomplete:
        print(f"⚠ Incomplete records (missing explanation/source): {len(incomplete)} -> {incomplete}")
    else:
        print(f"✅ All records have explanation + source URL!")

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sorted_records, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Written to {OUTPUT_FILE}")
    return len(missing) == 0 and len(incomplete) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
