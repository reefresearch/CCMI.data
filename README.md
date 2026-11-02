# CCMI.data

Complete GitHub-ready export of the CCMI Research Data catalogue, including the
current website, locally hosted observations, original uploads, FAIR metadata,
source inventory snapshots and reproducible Python build scripts.

## Included

- 24 catalogue records and 1,122 indexed file distributions.
- Search, resource/subject filters, study/file tabs, sorting and pagination.
- Leaflet map search; 65 DoE public mooring references; ICON site reference;
  tentative MF / Martha's Finyard site reference.
- Eight environmental logger series, with 105,679 timestamped observations:
  six ICON series (2026) and two MF HOBO series (2016).
- Temperature/light explorer, native/hourly/daily views, draggable date slider,
  statistics, CSV exports and selection provenance.
- Original XLSX/CSV uploads, derived CSV/GeoJSON, fonts, images and vendor assets.
- Per-study and per-file Markdown/JSON metadata, JSON-LD and metadata ZIP.
- Captured inventories for 14 external studies. Their data remain on their
  original repositories; this export includes the links, not external FASTQ,
  GitHub, Zenodo or Dryad data bytes.

## Open locally without rebuilding

Python 3.10+ is sufficient to prepare and serve the checked-in site:

```sh
python prepare_site.py
python -m http.server 8000 --directory site
```

Visit http://localhost:8000/. MF time series are at
http://localhost:8000/?page=explorer&site=mf.

Use an HTTP server rather than opening index.html directly; the explorer fetches
its observation JSON over HTTP. Map tiles and external repository downloads
need internet access; fonts and Leaflet code are included locally.

## Add to GitHub

Create an empty repository, unzip this export, and run these commands from its
`ccmi-data-github` directory. Replace the remote URL with your own repository:

```sh
git init
git add .
git commit -m "Import complete CCMI.data catalogue"
git branch -M main
git remote add origin "YOUR_GITHUB_REPOSITORY_URL"
git push -u origin main
```

Keep the complete directory structure, including `.github` and `.gitignore`.
`site/` is generated and ignored. `dist/`, `seed/`, `sources/` and the build
scripts are included in Git. Original data are therefore stored in the Git
repository for this interim self-contained export. Large future datasets can
be moved to object storage by updating distribution URLs and provenance.

This archive does not create a repository or publish anything to GitHub.

## Rebuild from included inputs

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python ingest.py seed dist/data
python build_catalog.py
python prepare_site.py
python validate_export.py
```

On Windows, activate with `.venv\Scripts\activate` instead. The original source
workbooks are in `seed/`; the DoE workbook, HOBO CSVs and external inventory
snapshots are under `sources/`. No files outside this export are needed.

`build_catalog.py` creates the catalogue, taxonomy, logger pack, record pages and
metadata. It retains the original source-host origin as a canonical identifier
input, preserving the existing file IDs. `prepare_site.py` copies `dist/` to
`site/` and rewrites local links and metadata URLs for the chosen host, without
changing file IDs or original data. It also rebuilds the metadata ZIP.
Always edit `dist/` or the Python inputs, then regenerate `site/`.

## DigitalOcean App Platform or another static host

For a root-hosted static site, use:

- Repository root: this project root.
- Build command: `python prepare_site.py`
- Output / publish directory: `site`

To include absolute URLs for a known host:

```sh
python prepare_site.py --origin https://data.example.org
```

Upload the contents of `site/` to any static web server. No database, Node build
or server application is required. `dist/` contains the original snapshot;
`site/` is the portable deployment output. No ChatGPT hosting project manifest,
Git credentials or Git history is included.

## Optional GitHub Pages

A manual-only `.github/workflows/pages.yml` workflow is included. In GitHub,
choose **Settings → Pages → Source: GitHub Actions**, then run
**Actions → Publish to GitHub Pages (manual) → Run workflow**. It obtains the
actual Pages origin/base path and prepares the correct asset/data URLs.
A push alone validates the project and does not invoke the Pages deployment.

For a project-path deployment, the equivalent preparation command is:

```sh
python prepare_site.py --origin https://YOUR_ORGANISATION.github.io --base-path /YOUR_REPOSITORY
```

Deploy `site/` at that same base path. To switch back to local/root hosting,
rerun `python prepare_site.py` without arguments. Preparation always starts
from `dist/`, so repeated runs do not double-prefix links.

Workflow references:
https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Access and reuse

The exported static site has **no built-in authentication**. The original
ChatGPT site's owner-only access does not transfer with the files, and the
“Private preview” badge is a display label, not an access control. Use a private
GitHub repository initially; configure access controls at your chosen host
before serving restricted data. A private source repository does not by itself
make the published website private.

No new licence is assigned to CCMI code, branding or unpublished data. Existing
third-party licences and source-specific metadata are retained. Font licences
are in `dist/fonts/`; Leaflet's licence is in `dist/vendor/LICENSE`.

FAIR metadata are preparation for stewardship, not a claim of certification.
Missing creators, contacts, permissions and licences remain unassigned.
Published paper and dataset DOIs remain separate from individual file IDs.

## Scientific interpretation

- ICON: 19.69960 N, -80.06058 W is a shared published site reference, not a
  verified logger/frame position. Depths are filename labels.
- MF: Martha's Finyard is a probable abbreviation match supported by the DoE
  mooring inventory and NCBI BioSample SAMN55782138. Its mapped coordinates
  (19.664867 N, -80.111183 W) are a tentative mooring/site reference. Deep/Mid
  are qualitative labels; depth in metres is unknown.
- DoE positions and MPA names reflect January 2023; current mooring condition
  and management boundaries are not asserted.
- Logger observations have no scientific QC exclusions or calibration
  adjustments applied. Observation coverage is not a verified deployment period.
- Time is interpreted at fixed UTC-05:00; MF's source CDT label and date-only
  midnight interpretation are documented. Light is lux, not PAR.
- Duplicate uploads are preserved, but byte-identical pairs are represented
  by one canonical series. Independent logger files are not merged.

## File layout

```text
.github/workflows/  Validation and optional manual Pages deployment
seed/              Twelve original ICON workbook uploads
sources/           HOBO originals, DoE workbook and repository snapshots
dist/              Complete editable/generated website snapshot
site/              Portable deployment output (generated; not in Git)
*.py               Import, catalogue, metadata and deployment scripts
requirements.txt   Python build dependency
EXPORT_INFO.json   Export provenance and content counts
SHA256SUMS.txt      Checksums for every included file except this manifest
```

The export is a working snapshot, not a live synchronisation with the hosted
site or its external source repositories.
