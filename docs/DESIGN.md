# diagram-ctl Design

## Purpose
Generate diagrams of the auto-ctl ecosystem from structured data files.
As the tool suite grows, diagrams should auto-update from data, not require manual drawing.

## Engine
Built on `diagrammer-x` (k4rlski/diagrammer-x):
- NetworkX for graph structure
- PyGraphviz → Graphviz `dot` engine for layout
- JSON input files → PNG output

## Data Model
`data/auto-ctl-ecosystem.json` contains:
- **tools[]**: all ctl tools with category, status, server, github, subtools
- **categories{}**: category metadata (color, description)
- **servers[]**: server nodes with IPs and roles

Adding a new tool = add one JSON entry → re-run → updated diagram.

## Diagram Views
Three views of the same data:
1. **Category view**: what each tool *does* (organized by function)
2. **Server view**: where each tool *runs* (organized by deployment)
3. **Pipeline view**: how tools *connect* (data flow for financial automation)

## Future
- YAML input support (same as JSON, just different loader)
- Slack posting: `diagram-ctl all --post #auto-ctl` 
- Auto-run on ecosystem changes (cron weekly or on git push)
- SVG output for web embedding (reports.permtrak.com widget)
