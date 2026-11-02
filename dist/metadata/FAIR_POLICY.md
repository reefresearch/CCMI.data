# CCMI Research Data: FAIR implementation policy (draft)

Status: proposed operational policy, pending institutional approval. Created 2026-10-29.

## Findable
Give each dataset a stable local identifier, a versioned landing page, rich metadata,
keywords and machine-readable Schema.org Dataset JSON-LD. Register a persistent
identifier (e.g. DOI through an established repository) before calling a record
fully FAIR. Local identifiers and hosted URLs are not registered DOIs.

## Accessible
Describe access conditions in the metadata and retrieve files through HTTPS.
Keep metadata available when data are restricted or withdrawn, with a tombstone
and reason. This seed site is private; it does not establish public accessibility.
No public release or reuse licence is implied by uploading a file here.

## Interoperable
Preserve original workbooks. Offer timestamped rows as CSV and metadata as JSON
and Markdown. Record variable definitions, units, timezone, missing-value rules,
instrument and provenance. Use ISO 8601 dates and WGS84 (EPSG:4326) coordinates
when verified. Map terms to CF/NERC vocabularies after scientific review; do not
assign seawater_temperature until deployment context confirms that measurement.
Retain both original column names and any approved standardized names.

## Reusable
Record creators, ORCIDs, rights holder, contact, explicit licence, collection
methods, calibration, deployment windows, quality flags, funding, permits,
processing history, version, checksum and suggested citation. Unknown fields
remain null, never inferred as verified. Pre/post-deployment observations must
be screened by the data steward. Light in lux is illuminance, not PAR.

## Release checklist
- Confirm authorship, rights holder, contact and permissions.
- Confirm site coordinates, coordinate precision, nominal depth and deployment dates.
- Resolve instrument changes and mismatches between observation sheets and Details.
- Document calibration, sensor accuracy, clock checks, missingness and quality flags.
- Review variable terms and publish a data dictionary and processing provenance.
- Choose an explicit data/code licence with the rights holder.
- Register a DOI, approve a citation and deposit a versioned preservation copy.
- Arrange steward ownership, backups, retention and metadata persistence.

This is FAIR-aligned preparation, not certification of FAIR compliance.
Reference: https://www.gofair.foundation/fair-principles
