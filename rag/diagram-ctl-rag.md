# diagram-ctl RAG
_Last updated: 2026-03-04 | Status: v0.1.0 dev_

## Purpose
Programmatic diagram generation for the auto-ctl tool ecosystem.
Reads structured JSON/YAML data files → renders PNG diagrams via GraphViz.
Built on `diagrammer-x` (k4rlski/diagrammer-x) — same NetworkX + PyGraphviz stack.

## Origin
- Base engine: `k4rlski/diagrammer-x` — Python + GraphViz, JSON input, renders PNG
- Karl built diagrammer-x for network/family tree diagrams; same rendering pipeline
- diagram-ctl adapts it for the tool ecosystem: categories, servers, pipelines

## Repos
- **diagram-ctl**: `k4rlski/diagram-ctl` (new)
- **diagrammer-x**: `k4rlski/diagrammer-x` (engine reference)

## Deploy Target
- **rodan.auto-cmd.io** → `/opt/auto-cmd/diagram-ctl/`
- Graphviz must be installed: `sudo apt install graphviz`
- Python: `pip install networkx pygraphviz`

## Commands
```bash
diagram-ctl category   # Tools grouped by category (Infrastructure/Financial/etc.)
diagram-ctl server     # Tools grouped by deployment server
diagram-ctl pipeline   # Financial automation pipeline diagram
diagram-ctl all        # All three diagrams at once → output/
```

## Diagram Types
1. **by-category**: LR layout, tools grouped under category headers, color = status
2. **by-server**: TB layout, tools under server nodes (claw/rodan/hiro/sitectl/etc.)
3. **pipeline**: Financial pipeline: EspoCRM → receipt-ctl/gmail-ctl → plaid-ctl → abcf-ctl → Dropbox/Slack

## Status Colors
| Color | Meaning |
|-------|---------|
| 🟢 Green #27AE60 | production |
| 🟡 Orange #F39C12 | dev |
| ⚪ Gray #95A5A6 | planned |
| ⬜ Light gray | concept |

## Data File
`data/auto-ctl-ecosystem.json` — source of truth for all tool metadata:
- 25 tools defined (as of 2026-03-04)
- Fields: id, name, tagline, category, version, status, server, slack_channel, github, subtools
- 7 servers defined with IPs, roles, colors
- 6 categories: Infrastructure, Financial, Communication, Intelligence, PERM_Product, DevOps

## Key Design Decisions
- Data-driven: update JSON → re-run → fresh diagrams (no code changes needed)
- Extends diagrammer-x engine exactly — same `to_agraph()` + `A.draw()` pattern
- YAML input also supported (future: add yaml loader alongside JSON)
- Output: PNG (default) — can extend to SVG/PDF via graphviz format param

## Tool Inventory (as of 2026-03-04)
### Infrastructure
bkup-ctl (v1.6, prod), dns-ctl (v1.2.0, prod), snapshot-ctl (v0.1.0, dev), log-ctl (planned)

### Financial  
receipt-ctl (v0.1.0, dev), plaid-ctl (v0.1.0, dev), abcf-ctl (v0.1.0, dev), vendor-ctl (planned), tax-ctl (planned)

### Communication
gmail-ctl (v0.1.0, dev), slack-ctl (planned), send-it (planned)

### Intelligence
context-ctl (running/prod), research-ctl (running/prod)

### PERM Product
site-ctl (v2.2.0, prod), swa-ctl (v0.1.0, dev), pwdx-daemon (prod), job-board-ctl (dev), media-ctl (planned)

### DevOps
repo-ctl (v0.1.0, dev), diagram-ctl (v0.1.0, dev), banner-ctl (installed/prod), parity-ctl (planned), fang-ctl (planned)

## MARS Integration (2026-05-10)

The static/server-rendered diagram approach in diagram-ctl (PNG via GraphViz) is complemented by interactive browser-based diagrams in mars-status:

- **`/ops/infra-dev`** — Infrastructure overview (Kanban lanes + SVG connectors)
- **`/diagrams/plan-ctl-workflow`** — Plan-CTL/Cursor-Export-CTL interop (lanes + PERT tabs)
- **`/diagrams/job-board-ctl-workflow`** — Job posting pipeline (lanes + PERT)
- **`/diagrams/migration-spear`** — Server migration diagram

These use HTML/CSS/SVG rendered client-side from JSON data files, without GraphViz. diagram-ctl remains the preferred approach for automated static exports.

### Deep Card Popups (2026-05-10)
Browser-based diagram popups support rich technical content:
- **Popup sections**: description, cron (actual crontab), queries[] (SQL), cli[] (commands), code[] (snippets), logs[] (commands), tech[], commands (chips), issues[], links[]
- **Detail pages**: `/diagrams/*/detail?card=<id>` — full-page render from same JSON data
- **Template**: `workflow-detail.html` (shared, parameterized)
- **Architecture**: One JSON file → modal popup + detail page (no per-card files)

### Logs Section + GitHub Source Links (2026-05-11)
New `logs[]` popup section type for diagram cards:
- **Schema**: Each entry has `label`, `path`, `host`, `view_cmd`, `grep_cmd`, `follow_cmd`
- **Rendering**: After code[], before issues[] — styled log entries with copyable commands
- **CSS**: `.dm-log-entry`, `.dm-log-badge`, `.dm-log-path`, `.dm-log-host`, `.dm-log-cmd` (and `.wd-` prefix in workflow-detail.html)
- **GitHub links on Kanban cards**: `github` field (repo + file + optional lines) now on all top-lane cards for clickable source links
- **Server fields**: `server` (host + path + service) added to cards with production presence
- **Populated on**: job-board-ctl-workflow Kanban cards (daemon, logfile, check-sched) + PERT steps (pj-cron, ba-check-sched, ba-wp-cron)
- **WordPress logs** (2026-05-11): Apache error log, PHP-FPM log, WP-cron access log added to wp-cli card and all WP-interacting PERT steps (pj-wpcli, ba-wp-future, ba-wp-cron, ba-check-sched, fe-wp-post)
- **Issue**: mars-status#130

### TOOL_META (ui-ctl.js)
- Path: `/tools/diagram-ctl`
- Repo: `k4rlski/diagram-ctl`
- RAG: `rag/diagram-ctl-rag.md`
