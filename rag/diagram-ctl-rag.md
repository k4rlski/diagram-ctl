# diagram-ctl RAG
_Last updated: 2026-06-06 | Status: v1.0.0 production_

## Purpose
Programmatic and browser-based diagram generation for the auto-ctl tool ecosystem.
Two rendering modes:
1. **CLI/GraphViz** — Python script reads JSON → renders PNG via NetworkX + PyGraphviz (rodan)
2. **Browser/MARS** — Interactive HTML diagrams with Kanban lanes + PERT tabs, powered by JSON data files

## Repos & Local Paths
| Item | Location |
|------|----------|
| GitHub | `k4rlski/diagram-ctl` |
| Local Clone | `/home/pyramider/DEVOPS Dropbox/DEVOPS-KARL/diagram-ctl/` |
| Engine Reference | `k4rlski/diagrammer-x` |
| MARS Diagrams (static) | `/home/pyramider/DEVOPS Dropbox/DEVOPS-KARL/MARS-STATUS/static/` |
| MARS JSON Data | `/home/pyramider/DEVOPS Dropbox/DEVOPS-KARL/MARS-STATUS/static/data/` |
| MARS Tool Page | `https://mars.auto-ctl.io/tools/diagram-ctl` |

## Architecture

### CLI Mode (GraphViz)
- Deploy: `rodan.auto-cmd.io` → `/opt/auto-cmd/diagram-ctl/`
- Dependencies: `graphviz`, `networkx`, `pygraphviz`
- Commands:
  ```bash
  diagram-ctl category   # Tools grouped by category
  diagram-ctl server     # Tools grouped by server
  diagram-ctl pipeline   # Financial pipeline flow
  diagram-ctl all        # Generate all → output/
  ```
- Data source: `data/auto-ctl-ecosystem.json`

### Browser Mode (MARS Interactive Diagrams)
- Served by MARS Flask app (`routes/pages.py`)
- Each diagram is a standalone HTML file in `static/`
- Data-driven: fetches JSON from `/static/data/<name>.json`
- Features: Server swimlanes (Kanban), PERT dependency charts, clickable nodes
- Routes registered in `routes/pages.py` lines 576–625

## Complete Diagram Inventory (10 diagrams)

### 1. Migration: Spear → CPX
| Field | Value |
|-------|-------|
| Route | `/diagrams/migration-spear` |
| File | `static/migration-spear.html` (245 lines) |
| Type | Static quad-panel migration diagram |
| Description | Shows the server migration path from Spear (legacy) to CPX (Akamai/Linode), with phases, services, and DNS cutover steps |

### 2. Plan-CTL Workflow
| Field | Value |
|-------|-------|
| Route | `/diagrams/plan-ctl-workflow` |
| File | `static/plan-ctl-workflow.html` (837 lines) |
| Data | `static/data/plan-ctl-workflow.json` |
| Type | Kanban lanes + PERT |
| Description | Visualizes plan-ctl lifecycle: plan creation → task breakdown → execution → completion. Server lanes show where each phase runs. PERT shows dependencies between plan stages. |

### 3. Job-Board-CTL Workflow
| Field | Value |
|-------|-------|
| Route | `/diagrams/job-board-ctl-workflow` |
| File | `static/job-board-ctl-workflow.html` (834 lines) |
| Data | `static/data/job-board-ctl-workflow.json` |
| Type | Kanban lanes + PERT |
| Description | Job board automation: source scraping → filtering → application → tracking. Shows crawler pipeline, resume selection, and application dispatch across servers. |

### 4. User Mgmt
| Field | Value |
|-------|-------|
| Route | `/diagrams/user-mgmt` |
| File | `static/user-mgmt.html` (837 lines) |
| Data | `static/data/user-mgmt.json` |
| Type | Kanban lanes + PERT |
| Description | User management workflow: account provisioning, role assignment, access control, and audit trails across infrastructure servers. |

### 5. APX-CTL Workflow
| Field | Value |
|-------|-------|
| Route | `/diagrams/apx-ctl-workflow` |
| File | `static/apx-ctl-workflow.html` (837 lines) |
| Data | `static/data/apx-ctl-workflow.json` |
| Type | Kanban lanes + PERT |
| Description | APX (Apex Financial) automation: receipt capture → categorization → QuickBooks sync → reconciliation. Financial pipeline across EspoCRM and processing servers. |

### 6. Auto-Print Workflow
| Field | Value |
|-------|-------|
| Route | `/diagrams/auto-print-workflow` |
| File | `static/auto-print-workflow.html` (837 lines) |
| Data | `static/data/auto-print-workflow.json` |
| Type | Kanban lanes + PERT |
| Description | Automated print pipeline: document generation → queue management → printer dispatch → confirmation. Covers label printing, envelope addressing, and bulk mailings. |

### 7. Notify-CTL Workflow
| Field | Value |
|-------|-------|
| Route | `/diagrams/notify-ctl-workflow` |
| File | `static/notify-ctl-workflow.html` (837 lines) |
| Data | `static/data/notify-ctl-workflow.json` |
| Type | Kanban lanes + PERT |
| Description | Notification orchestration: event triggers → routing logic → multi-channel dispatch (Slack, email, SMS, Telegram). Shows alert escalation and delivery confirmation. |

### 8. Site-CTL Workflow
| Field | Value |
|-------|-------|
| Route | `/diagrams/site-ctl-workflow` |
| File | `static/site-ctl-workflow.html` (880 lines) |
| Data | `static/data/site-ctl-workflow.json` |
| Type | Kanban lanes + PERT |
| Description | Site management: domain provisioning → SSL/DNS → deployment → monitoring. Covers WordPress, static sites, and reverse proxy configuration across all servers. |

### 9. Service-CTL Workflow
| Field | Value |
|-------|-------|
| Route | `/diagrams/service-ctl-workflow` |
| File | `static/service-ctl-workflow.html` (588 lines) |
| Data | `static/data/service-ctl-workflow.json` |
| Type | Kanban lanes + PERT |
| Description | Service lifecycle management: systemd unit control, health checks, restart policies, and cross-server orchestration. Shows service dependencies and startup ordering. |

### 10. Mail-CTL Workflow
| Field | Value |
|-------|-------|
| Route | `/diagrams/mail-ctl-workflow` |
| File | `static/mail-ctl-workflow.html` (587 lines) |
| Data | `static/data/mail-ctl-workflow.json` |
| Type | Kanban lanes + PERT |
| Description | Email infrastructure workflow: account management → forwarding rules → inbox operations → monitoring. Shows Dovecot/Postfix interactions and spam filtering pipeline. |

## Diagram HTML Template Pattern
All workflow diagrams (items 2–10) share a common structure:
1. CSS variables + dark/light theme support
2. Server swimlanes section (`.server-lanes`) — horizontal Kanban columns per server
3. PERT section (`.pert-section`) — dependency graph with nodes and arrows
4. JSON fetch on load → renders cards into lanes, builds PERT connections
5. Detail sub-route (`/detail`) for expanded view (uses `workflow-detail.html`)

## JSON Data Schema
Each `static/data/<name>.json` follows:
```json
{
  "title": "Workflow Name",
  "servers": [
    {"id": "server-id", "name": "Display Name", "color": "#hex"}
  ],
  "lanes": [
    {
      "server": "server-id",
      "cards": [
        {"id": "card-id", "title": "...", "status": "active|pending|done", "desc": "..."}
      ]
    }
  ],
  "pert": {
    "nodes": [{"id": "...", "label": "...", "x": 0, "y": 0}],
    "edges": [{"from": "...", "to": "...", "label": "..."}]
  }
}
```

## Status Colors (CLI mode)
| Color | Meaning |
|-------|---------|
| Green #27AE60 | production |
| Orange #F39C12 | dev |
| Gray #95A5A6 | planned |
| Light gray | concept |

## CLI Data File
`data/auto-ctl-ecosystem.json` — 25+ tools defined with:
- Fields: id, name, tagline, category, version, status, server, slack_channel, github, subtools
- 7 servers: claw, rodan, hiro, sitectl, hermes, cpx42, cpx43
- 6 categories: Infrastructure, Financial, Communication, Intelligence, PERM_Product, DevOps

## MARS Integration
- Menu location: Diagrams dropdown in top nav (`static/ui-ctl.js` lines 161–170)
- Tool page: `/tools/diagram-ctl` → `static/diagram-ctl.html`
- Routes: `routes/pages.py` lines 576–625
- Master diagram: `/master-diagram` → `static/master-diagram.html` (ecosystem overview)

## Planned Additions
- `/diagrams/hermes-ctl-workflow` — Hermes agent messaging + memory workflow
- `/diagrams/vpn-ctl-workflow` — VPN tunnel management diagram

## GitHub Issues
Track at: https://github.com/k4rlski/diagram-ctl/issues

## Related Tools
- **plan-ctl**: Plans reference diagrams for visualization
- **context-ctl**: ChromaDB indexes this RAG for retrieval
- **mars-status**: Hosts all browser diagrams
- **diagrammer-x**: Original GraphViz rendering engine
