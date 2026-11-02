---
identifier: "ccmi-env-003"
title: "ICON 18 m — temperature & light"
category: "environmental"
metadata_status: "draft"
metadata_version: "0.1.0"
metadata_created: "2026-10-29"
source_file: "ICON_18m.xlsx"
source_sha256: "a5faf206bf2c68cf8a5a2af4acb712477d21929ba11c11ce9d4c8224163eb0e6"
equivalent_files: ["ICON_18m.xlsx", "ICON_18m_26-10-26.xlsx"]
landing_page: "https://ccmi-research-data.g-roff.chatgpt.site/records/ccmi-env-003.html"
persistent_identifier: null
creators: null
rights_holder: null
contact: null
license: null
access: "owner-private seed repository; release pending steward approval"
nominal_depth_m: 18
depth_verified: false
latitude: 19.6996
longitude: -80.06058
spatial_reference: "EPSG:4326 assumed for mapping; source datum not stated"
temporal_start: "2026-03-11T09:00:00-05:00"
temporal_end: "2026-10-23T13:30:00-05:00"
temporal_basis: "populated observation timestamps, not confirmed in-water period"
sampling_interval_minutes_mode: 15.0
instrument_product_in_details: "Not documented"
instrument_serial_in_details_or_header: "10383248 (header)"
keywords: ["environmental", "ICON", "temperature", "illuminance"]
quality_control: "not applied"
related_csv: "../data/ICON_18m.csv"
coordinates: [19.6996, -80.06058]
location: "ICON nursery series, Little Cayman — ICON Reef site reference"
coordinate_basis: "Published ICON Reef monitoring-site coordinate, assigned to the ICON nursery series by the data steward on 2026-10-30. Exact nursery-frame and logger positions are unverified."
coordinate_source: "Foster & Foster (2018), Demographics and Population Dynamics Project the Future of Hard Coral Assemblages in Little Cayman, Table 1."
coordinate_source_url: "https://www.scirp.org/journal/paperinformation?paperid=82210"
coordinate_scope: "shared site reference; not an individual deployment position"
coordinate_uncertainty_m: null
coordinate_datum: "WGS84 assumed for mapping; source datum not stated"
subjects: ["environmental-conditions"]
subject_labels: ["Environmental conditions"]
subject_basis: "Curated from catalog study description; steward review pending."
subject_vocabulary: "ccmi-subjects:1.0.0"
resource_types: ["data"]
---

# ICON 18 m — temperature & light

Logger observations labelled ICON at nominal 18 m. The populated observation rows span 2026-03-11 to 2026-10-23, with 21,715 timestamped records and a modal sampling interval of 15 minutes. Deployment location and quality control require steward review.

## Provenance and equivalence

Imported without modifying original bytes. SHA-256 identifies both supplied names as byte-identical copies, not separate versions. The CSV retains original headers, timestamp strings and every timestamped row; rows without a timestamp are excluded. No averaging, timezone conversion, unit conversion, interpolation or quality filtering is applied. Data and device-summary date ranges may differ.

## Data dictionary

| Original column | Definition | Units | Populated | Missing |
| --- | --- | --- | ---: | ---: |
| # | Sample index | 1 | 21715 | 0 |
| Date Time, GMT-05:00 | Observation time | UTC−05:00 | 21715 | 0 |
| Temp, °C (LGR S/N: 10383248, SEN S/N: 10383248) | Temperature | °C | 21715 | 0 |
| Intensity, Lux (LGR S/N: 10383248, SEN S/N: 10383248) | Illuminance | lux | 21715 | 0 |

## Quality and interpretation

- Original observations are not quality controlled. Individual deployment positions and actual in-water deployment windows require confirmation.
- Nominal depth is inferred from the filename; instrument depth is unverified.
- Initial temperatures reach 35.756 °C. Confirm deployment timing and screen handling/air exposure before ecological interpretation.
- Light values are illuminance in lux; no PAR conversion has been applied.
- Published ICON Reef monitoring-site coordinate, assigned to the ICON nursery series by the data steward on 2026-10-30. Exact nursery-frame and logger positions are unverified.
- Duplicate timestamps: 0; non-increasing timestamp steps: 0.

## Methods and instruments

Instrument metadata below are reproduced from the workbook Details sheet or header and require confirmation against deployment records.

```json
{}
```

## Citation and rights

Draft citation: [Creator pending]. (2026). ICON 18 m — temperature & light (draft version 0.1.0). CCMI Research Data. Local identifier: ccmi-env-003. A DOI and final citation have not been assigned. Data ownership, authorship and licence require confirmation. No open reuse licence is granted.

## FAIR readiness

- Findable: local identifier, landing page, catalog indexing and rich metadata supplied; DOI registration pending.
- Accessible: HTTPS distribution in private site; release conditions require approval and metadata retention must be operationally guaranteed.
- Interoperable: original XLSX, CSV, JSON-LD and variable dictionary supplied; controlled vocabulary review pending.
- Reusable: provenance, SHA-256 and missingness documented; licence, authors, coordinates, deployment methods, calibration, quality control and funding/permits remain to be completed.

See [draft FAIR policy](FAIR_POLICY.md). This record is not fully FAIR-compliant.
