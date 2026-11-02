---
identifier: "ccmi-code-001"
category: "code"
version: "0.1.0-draft"
license: null
creator: null
contact: null
sha256: "8198d0b1225f8b0da15df6ce1ab46cd06745d78b5164b71ba1301481757735e9"
subjects: ["environmental-conditions"]
subject_labels: ["Environmental conditions"]
subject_basis: "Curated from catalog study description; steward review pending."
subject_vocabulary: "ccmi-subjects:1.0.0"
resource_types: ["code", "documentation"]
---

# Logger export ingestion

Reproducible Python importer for the seed workbooks. Checks SHA-256 equivalence, extracts timestamped rows to CSV and records observed temporal coverage and missingness.

## Run

```sh
python -m pip install -r requirements.txt
python ingest.py INPUT_DIRECTORY OUTPUT_DIRECTORY
```

## Provenance

Created for this repository on 2026-10-29. Inputs are original XLSX workbooks. Outputs: inventory.json and one CSV for each SHA-256-distinct workbook. Timestamp strings, headers, numeric values and missing cells are preserved for all rows with timestamps. Device metadata comes from the Details worksheet when present. No quality flags, averaging or conversion are introduced.

## FAIR readiness

Stable local identifier, catalog record, documented requirements and SHA-256 supplied. Registered persistent identifier, steward contact, approved authorship, licence and long-term preservation remain pending. Related data: ccmi-env-001 through ccmi-env-006. See FAIR_POLICY.md.
