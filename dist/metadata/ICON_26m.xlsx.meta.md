---
identifier: "ccmi-env-005"
title: "ICON 26 m — temperature & light · Apr–Oct"
category: "environmental"
metadata_status: "draft"
metadata_version: "0.1.0"
metadata_created: "2026-10-29"
source_file: "ICON_26m.xlsx"
source_sha256: "bf88442b9b4e1ade3a9f53ed847ca7f622a163d854474874671962e48f724285"
equivalent_files: ["ICON_26_26-10-26m.xlsx", "ICON_26m.xlsx"]
landing_page: "https://ccmi-research-data.g-roff.chatgpt.site/records/ccmi-env-005.html"
persistent_identifier: null
creators: null
rights_holder: null
contact: null
license: null
access: "owner-private seed repository; release pending steward approval"
nominal_depth_m: 26
depth_verified: false
latitude: 19.6996
longitude: -80.06058
spatial_reference: "EPSG:4326 assumed for mapping; source datum not stated"
temporal_start: "2026-04-24T10:00:00-05:00"
temporal_end: "2026-10-23T13:15:00-05:00"
temporal_basis: "populated observation timestamps, not confirmed in-water period"
sampling_interval_minutes_mode: 15.0
instrument_product_in_details: "MX2202"
instrument_serial_in_details_or_header: "22264297"
keywords: ["environmental", "ICON", "temperature", "illuminance"]
quality_control: "not applied"
related_csv: "../data/ICON_26_26-10-26m.csv"
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

# ICON 26 m — temperature & light · Apr–Oct

Logger observations labelled ICON at nominal 26 m. The populated observation rows span 2026-04-24 to 2026-10-23, with 17,479 timestamped records and a modal sampling interval of 15 minutes. Deployment location and quality control require steward review.

## Provenance and equivalence

Imported without modifying original bytes. SHA-256 identifies both supplied names as byte-identical copies, not separate versions. The CSV retains original headers, timestamp strings and every timestamped row; rows without a timestamp are excluded. No averaging, timezone conversion, unit conversion, interpolation or quality filtering is applied. Data and device-summary date ranges may differ.

## Data dictionary

| Original column | Definition | Units | Populated | Missing |
| --- | --- | --- | ---: | ---: |
| # | Sample index | 1 | 6341 | 11138 |
| Date-Time (EST) | Observation time | UTC−05:00 | 17479 | 0 |
| Temperature , °C | Temperature | °C | 17479 | 0 |
| Light , lux | Illuminance | lux | 8634 | 8845 |

## Quality and interpretation

- Original observations are not quality controlled. Individual deployment positions and actual in-water deployment windows require confirmation.
- Nominal depth is inferred from the filename; instrument depth is unverified.
- Device Details describe an export segment; the Data sheet may contain edits or appended observations. Do not extend instrument attribution beyond the documented segment without confirmation.
- Missing measurements occur in timestamped rows; see per-variable counts. Blank cells remain empty in CSV.
- Light values are illuminance in lux; no PAR conversion has been applied.
- Published ICON Reef monitoring-site coordinate, assigned to the ICON nursery series by the data steward on 2026-10-30. Exact nursery-frame and logger positions are unverified.
- Duplicate timestamps: 0; non-increasing timestamp steps: 0.

## Methods and instruments

Instrument metadata below are reproduced from the workbook Details sheet or header and require confirmation against deployment records.

```json
{
  "App Name": "HOBOconnect",
  "Version": "2.10.1 (1779452022)",
  "Product": "MX2202",
  "Serial Number": "22264297",
  "Firmware Version": "70.140",
  "Manufacturer": "Onset Computer Corporation",
  "Device Memory": "176128",
  "Header Created": "2026/04/24 09:56:13 EST",
  "Name": "ICON26m-22264297",
  "Location": "Off",
  "Group Name": "Nursery",
  "Deployment Number": "3",
  "Never Stop (Overwrites Old Data) Enabled": "No",
  "Configure Date": "2026/04/24 09:56:13 EST",
  "Logging Interval": "0 hour 15 minutes 0 seconds",
  "Logging Mode": "Fixed - Normal",
  "Start Logging": "On Date/Time 2026/04/24 10:00:00 EST",
  "Stop Logging": "Stop When Memory Fills , Stop on Button Push ",
  "Show Visual Alarms Until": "Sensors In Limits",
  "Show LED": "On",
  "Bluetooth Always On": "Off",
  "Upload Data Via": "Off",
  "High Alarm Value": "Not Configured",
  "Low Alarm Value": "Not Configured",
  "Samples": "6343",
  "Max": "21657.60",
  "Min": ".00",
  "Avg": "2410.76",
  "Std Dev": "3969.26",
  "First Sample Time": "2026/04/24 10:00:00 EST",
  "Last Sample Time": "2026/06/29 11:30:00 EST"
}
```

## Citation and rights

Draft citation: [Creator pending]. (2026). ICON 26 m — temperature & light · Apr–Oct (draft version 0.1.0). CCMI Research Data. Local identifier: ccmi-env-005. A DOI and final citation have not been assigned. Data ownership, authorship and licence require confirmation. No open reuse licence is granted.

## FAIR readiness

- Findable: local identifier, landing page, catalog indexing and rich metadata supplied; DOI registration pending.
- Accessible: HTTPS distribution in private site; release conditions require approval and metadata retention must be operationally guaranteed.
- Interoperable: original XLSX, CSV, JSON-LD and variable dictionary supplied; controlled vocabulary review pending.
- Reusable: provenance, SHA-256 and missingness documented; licence, authors, coordinates, deployment methods, calibration, quality control and funding/permits remain to be completed.

See [draft FAIR policy](FAIR_POLICY.md). This record is not fully FAIR-compliant.
