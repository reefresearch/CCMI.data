---
id: "ccmi-file-8cc2a86ebf7254a6"
parent_id: "ccmi-env-008"
title: "HOBO_MF_Mid_2016.csv"
name: "HOBO_MF_Mid_2016.csv"
url: "https://ccmi-research-data.g-roff.chatgpt.site/data/HOBO_MF_Mid_2016.csv"
repository_url: "https://ccmi-research-data.g-roff.chatgpt.site/records/ccmi-env-008.html"
provider: "CCMI · normalized observations"
version: "0.1.0-draft"
kind: "data"
category: "environmental"
format: "CSV"
size_bytes: 334041
checksum: "89c209885c308ade08bdae0a71d8af2e7c9ff4d205b7e58ce473254cd15e1de4"
checksum_type: "sha256"
source_license: null
paper_doi: null
dataset_doi: null
concept_doi: null
doi_scope: "No paper or dataset DOI established for this source."
landing: "/?file=ccmi-file-8cc2a86ebf7254a6"
metadata: "file-records/ccmi-file-8cc2a86ebf7254a6.meta.md"
metadata_json: "file-records/ccmi-file-8cc2a86ebf7254a6.json"
metadata_checked: "2026-10-30"
link_status: "Hosted file; checksum verified against supplied source or generated normalization. Scientific QC not applied."
external: false
variables: ["Temperature"]
depth: null
depth_label: "Mid"
start: "2016-06-21 11:00:00"
end: "2016-10-05 14:15:00"
timezone: "Central Daylight Time (source label); interpreted UTC−05:00"
instrument: "UA-002-64 / USB PID 289"
serial: "10701513"
deployment_description: "MF-MID-47"
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
subject_basis: "Filename and repository context; code, documentation and archives inherit study subjects. Steward review pending."
subject_vocabulary: "ccmi-subjects:1.0.0"
resource_types: ["data"]
---

# HOBO_MF_Mid_2016.csv

Probable identification: MF = Martha's Finyard. NCBI BioSample SAMN55782138 uses MF in its sample name, explicitly names Martha's Finyard, and reports 19.66487 N, 80.11118 W. These agree with the supplied DoE January 2023 mooring 237 coordinates. This supports an abbreviation match, not confirmation of the 2016 deployment or logger positions.

Deep / Mid and MF-BOT-46 / MF-MID-47 are source labels. Numeric water depths and the meanings of 46 / 47 are not established.

Source timezone_label is Central Daylight Time, interpreted as fixed UTC−05:00 for this June–October export. Logger clock settings are unverified; original timestamp strings are retained.

Date-only source timestamp strings are interpreted as 00:00:00 on that date; original strings are retained.

Temperature values are used as supplied. raw_temperature is retained in the originals; its units and conversion/calibration history are not established.

No quality-control exclusions, calibration corrections or deployment-window screening applied. Observation coverage is not a verified in-water period.

Two uploads per series have identical SHA-256 hashes. All originals are retained; only one canonical original and one normalized CSV are indexed per series.

Normalization adds a sequential sample index and selects timestamp and temperature_c without rounding or changing timestamp strings. Full source metadata and raw_temperature remain in the original CSV.