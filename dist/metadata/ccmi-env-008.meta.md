---
id: "ccmi-env-008"
hobo: true
external: true
category: "environmental"
categories: ["environmental"]
title: "MF HOBO Mid — temperature · Jun–Oct 2016"
description: "HOBO temperature observations labelled MF-MID-47: 10,190 timestamped records from 2016-06-21 to 2016-10-05, at a modal 15-minute interval. MF probably refers to Martha's Finyard; the mapped position is a tentative site reference. Mid is a source depth label; depth in metres is unknown."
depth: null
depth_label: "Mid"
depth_basis: "qualitative source label; numeric depth not established"
variables: ["Temperature"]
site_id: "mf"
site_label: "MF · probably Martha's Finyard"
start: "2016-06-21 11:00:00"
end: "2016-10-05 14:15:00"
records: 10190
interval: 15.0
timezone: "Central Daylight Time (source label); interpreted UTC−05:00"
timezone_interpretation: "UTC−05:00 assumed from source CDT label for June–October 2016; clock configuration unverified"
format: ["CSV"]
status: "Location inferred · review pending"
license: null
creator: null
contact: null
paper_doi: null
dataset_doi: null
concept_doi: null
doi: null
paper_title: null
paper_year: null
paper_authors: []
dataset_creators: []
paper_relationship_status: "No paper association established for these uploads."
repository_accession: null
repository_url: "https://ccmi-research-data.g-roff.chatgpt.site/?page=explorer&site=mf"
source_repositories: [{"provider": "CCMI · supplied HOBO exports", "url": "https://ccmi-research-data.g-roff.chatgpt.site/?content=files&study=ccmi-env-008", "version": "2026-10-30"}]
version: "0.1.0-draft"
metadata_checked: "2026-10-30"
instrument: "UA-002-64 / USB PID 289"
serial: "10701513"
deployment_description: "MF-MID-47"
notes: ["Probable identification: MF = Martha's Finyard. NCBI BioSample SAMN55782138 uses MF in its sample name, explicitly names Martha's Finyard, and reports 19.66487 N, 80.11118 W. These agree with the supplied DoE January 2023 mooring 237 coordinates. This supports an abbreviation match, not confirmation of the 2016 deployment or logger positions.", "Deep / Mid and MF-BOT-46 / MF-MID-47 are source labels. Numeric water depths and the meanings of 46 / 47 are not established.", "Source timezone_label is Central Daylight Time, interpreted as fixed UTC−05:00 for this June–October export. Logger clock settings are unverified; original timestamp strings are retained.", "Date-only source timestamp strings are interpreted as 00:00:00 on that date; original strings are retained.", "Temperature values are used as supplied. raw_temperature is retained in the originals; its units and conversion/calibration history are not established.", "No quality-control exclusions, calibration corrections or deployment-window screening applied. Observation coverage is not a verified in-water period.", "Two uploads per series have identical SHA-256 hashes. All originals are retained; only one canonical original and one normalized CSV are indexed per series."]
aliases: ["161005_CCMI_HOBO_MF_Mid October 2016.csv", "161005_CCMI_HOBO_MF_Mid October 2016(1).csv"]
sha256: "0a40cefbec9e2eac07b1523c2ef891f18ac6d0a09f45e7f1cddc27f6635a9f7d"
bytes: 1099318
csv: "HOBO_MF_Mid_2016.csv"
csv_sha256: "89c209885c308ade08bdae0a71d8af2e7c9ff4d205b7e58ce473254cd15e1de4"
metadata: "ccmi-env-008.meta.md"
landing: "/records/ccmi-env-008.html"
temperature_summary: {"valid": 10190, "missing": 0, "minimum": 29.452, "maximum": 31.37}
coordinates: [19.664867, -80.111183]
latitude: 19.664867
longitude: -80.111183
location: "Martha's Finyard, Little Cayman — probable MF site reference"
coordinate_basis: "Probable identification: MF = Martha's Finyard. NCBI BioSample SAMN55782138 uses MF in its sample name, explicitly names Martha's Finyard, and reports 19.66487 N, 80.11118 W. These agree with the supplied DoE January 2023 mooring 237 coordinates. This supports an abbreviation match, not confirmation of the 2016 deployment or logger positions."
coordinate_source: "Cayman Islands DoE public moorings, January 2023, ID 237; abbreviation corroborated by NCBI BioSample SAMN55782138 (2023 samples)."
coordinate_source_url: "https://www.ncbi.nlm.nih.gov/biosample/SAMN55782138"
coordinate_sources: ["https://doe.ky/resources/public-moorings/", "https://www.ncbi.nlm.nih.gov/biosample/SAMN55782138"]
coordinate_scope: "tentative site / mooring reference; not a verified logger position"
coordinate_datum: "WGS84 assumed for mapping; source datum not specified"
coordinate_uncertainty_m: null
location_status: "inferred; steward confirmation required"
subjects: ["environmental-conditions"]
subject_labels: ["Environmental conditions"]
subject_basis: "Curated from catalog study description; steward review pending."
subject_vocabulary: "ccmi-subjects:1.0.0"
resource_types: ["data"]
---

# MF HOBO Mid — temperature · Jun–Oct 2016

HOBO temperature observations labelled MF-MID-47: 10,190 timestamped records from 2016-06-21 to 2016-10-05, at a modal 15-minute interval. MF probably refers to Martha's Finyard; the mapped position is a tentative site reference. Mid is a source depth label; depth in metres is unknown.

## Provenance and location inference

Probable identification: MF = Martha's Finyard. NCBI BioSample SAMN55782138 uses MF in its sample name, explicitly names Martha's Finyard, and reports 19.66487 N, 80.11118 W. These agree with the supplied DoE January 2023 mooring 237 coordinates. This supports an abbreviation match, not confirmation of the 2016 deployment or logger positions.

Deep / Mid and MF-BOT-46 / MF-MID-47 are source labels. Numeric water depths and the meanings of 46 / 47 are not established.

Source timezone_label is Central Daylight Time, interpreted as fixed UTC−05:00 for this June–October export. Logger clock settings are unverified; original timestamp strings are retained.

Date-only source timestamp strings are interpreted as 00:00:00 on that date; original strings are retained.

Temperature values are used as supplied. raw_temperature is retained in the originals; its units and conversion/calibration history are not established.

No quality-control exclusions, calibration corrections or deployment-window screening applied. Observation coverage is not a verified in-water period.

Two uploads per series have identical SHA-256 hashes. All originals are retained; only one canonical original and one normalized CSV are indexed per series.

Location evidence: [https://www.ncbi.nlm.nih.gov/biosample/SAMN55782138](https://www.ncbi.nlm.nih.gov/biosample/SAMN55782138); DoE January 2023 inventory, mooring 237.

## Data dictionary

| Column | Definition | Units | Valid | Missing |
| --- | --- | --- | ---: | ---: |
| timestamp | Observation timestamp (source wall time) | not specified / not applicable | 10190 | 0 |
| temperature_c | Temperature, supplied in degrees Celsius | °C | 10190 | 0 |
| raw_temperature | Raw source value; units and conversion unverified | not specified / not applicable | 10190 | 0 |
| supported_model | Source model label | not specified / not applicable | 10190 | 0 |
| serial_number | Logger serial number | not specified / not applicable | 10190 | 0 |
| deployment_description | Source deployment label | not specified / not applicable | 10190 | 0 |
| logging_interval_seconds | Source logging interval in seconds | s | 10190 | 0 |
| timezone_label | Source timezone label | not specified / not applicable | 10190 | 0 |

## FAIR preparation

Findable: local identifiers and searchable metadata; DOI not registered. Accessible: original and normalized CSVs on this site, subject to site access. Interoperable: documented units, source labels and timezone interpretation; machine-readable JSON-LD. Reusable: SHA-256, original metadata, provenance and provisional location supplied; authorship, reuse licence, deployment depths, clock configuration, collection methods and QC await confirmation. No open reuse licence is implied.
