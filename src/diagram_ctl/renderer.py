"""
diagram-ctl renderer — generates diagrams from auto-ctl-ecosystem.json
Built on diagrammer-x (k4rlski/diagrammer-x): NetworkX + PyGraphviz + Graphviz
"""

import json
from pathlib import Path
import networkx as nx

STATUS_COLORS = {
    "production": "#27AE60",
    "dev":        "#F39C12",
    "planned":    "#95A5A6",
    "concept":    "#BDC3C7",
}

STATUS_STYLE = {
    "production": "filled",
    "dev":        "filled,dashed",
    "planned":    "filled,dotted",
    "concept":    "filled,dotted",
}


def load_ecosystem(path: str) -> dict:
    return json.loads(Path(path).read_text())


def render_by_category(data: dict, output_path: str):
    """Group tools by category in a hierarchical diagram."""
    try:
        from networkx.drawing.nx_agraph import to_agraph
    except ImportError:
        raise RuntimeError("pygraphviz not installed: pip install pygraphviz")

    G = nx.DiGraph()
    cats = data["categories"]
    tools = data["tools"]

    # Category header nodes
    for cat_id, cat in cats.items():
        G.add_node(cat_id,
            label=cat_id.replace("_", " "),
            shape="box", style="filled,bold",
            fillcolor=cat["color"], fontcolor=cat["text_color"],
            fontsize="14", width="3", height="0.6"
        )

    # Tool nodes
    for t in tools:
        node_id = t["id"]
        cat = cats.get(t["category"], {})
        fill = STATUS_COLORS.get(t["status"], "#BDC3C7")
        label = f'{t["name"]}\\n{t["version"]}\\n{t["status"]}'
        G.add_node(node_id,
            label=label,
            shape="rectangle", style=STATUS_STYLE.get(t["status"], "filled"),
            fillcolor=fill, fontcolor="white",
            fontsize="10", width="2.2", height="0.65"
        )
        G.add_edge(t["category"], node_id)

        # Subtools
        for sub in t.get("subtools", []):
            G.add_node(sub, label=sub, shape="ellipse", style="filled",
                       fillcolor="#D5DBDB", fontsize="9", width="1.5", height="0.4")
            G.add_edge(node_id, sub)

    A = to_agraph(G)
    A.graph_attr.update(rankdir="LR", splines="ortho", nodesep="0.5",
                        ranksep="1.2", bgcolor="white",
                        label=f'auto-ctl Ecosystem — {data["meta"]["version"]}',
                        fontsize="18", labelloc="t")
    A.layout("dot")
    A.draw(output_path, format="png")
    print(f"✅ Written: {output_path}")


def render_by_server(data: dict, output_path: str):
    """Show tools grouped by deployment server."""
    try:
        from networkx.drawing.nx_agraph import to_agraph
    except ImportError:
        raise RuntimeError("pygraphviz not installed")

    G = nx.DiGraph()
    servers = {s["id"]: s for s in data["servers"]}
    tools = data["tools"]

    # Server header nodes
    for sid, s in servers.items():
        G.add_node(sid,
            label=f'{s["host"]}\\n{s["role"]}',
            shape="box3d", style="filled",
            fillcolor=s["color"], fontcolor="white",
            fontsize="12", width="2.8", height="0.7"
        )

    # Map server host → id
    host_to_id = {s["host"]: s["id"] for s in data["servers"]}
    host_to_id["all"] = None  # banner-ctl goes to all

    # Tool nodes
    for t in tools:
        node_id = t["id"]
        fill = STATUS_COLORS.get(t["status"], "#BDC3C7")
        label = f'{t["name"]}\\n{t["tagline"][:28]}'
        G.add_node(node_id,
            label=label, shape="rectangle", style="filled",
            fillcolor=fill, fontcolor="white", fontsize="9",
            width="2.2", height="0.55"
        )
        srv_host = t.get("server", "")
        srv_id = host_to_id.get(srv_host)
        if srv_id:
            G.add_edge(srv_id, node_id)

    A = to_agraph(G)
    A.graph_attr.update(rankdir="TB", splines="ortho",
                        label=f'auto-ctl Tools by Server — {data["meta"]["version"]}',
                        fontsize="18", labelloc="t", bgcolor="white")
    A.layout("dot")
    A.draw(output_path, format="png")
    print(f"✅ Written: {output_path}")


def render_pipeline(data: dict, output_path: str):
    """Financial pipeline: plaid-ctl, abcf-ctl, receipt-ctl, gmail-ctl."""
    try:
        from networkx.drawing.nx_agraph import to_agraph
    except ImportError:
        raise RuntimeError("pygraphviz not installed")

    G = nx.DiGraph()

    pipeline = [
        ("EspoCRM", "CRM\\n(read-only)", "#3498DB"),
        ("receipt-ctl", "receipt-ctl\\nVendor invoices", "#27AE60"),
        ("gmail-ctl", "gmail-ctl\\nEmail search", "#8E44AD"),
        ("plaid-ctl", "plaid-ctl\\nBank transactions", "#E67E22"),
        ("abcf-ctl", "abcf-ctl\\nAd billing confirm", "#C0392B"),
        ("Dropbox", "Dropbox\\nReceipt storage", "#2980B9"),
        ("Slack", "Slack\\nAlerts", "#4A154B"),
    ]

    for nid, label, color in pipeline:
        G.add_node(nid, label=label, shape="rectangle", style="filled",
                   fillcolor=color, fontcolor="white", fontsize="11",
                   width="2.5", height="0.7")

    edges = [
        ("EspoCRM", "receipt-ctl", "vendor list"),
        ("EspoCRM", "abcf-ctl", "confirmed cases"),
        ("EspoCRM", "plaid-ctl", "invoiced cases"),
        ("receipt-ctl", "Dropbox", "PDF upload"),
        ("gmail-ctl", "abcf-ctl", "email receipt"),
        ("plaid-ctl", "abcf-ctl", "bank match"),
        ("abcf-ctl", "Slack", "confirmation"),
        ("plaid-ctl", "Slack", "reconcile alert"),
    ]

    for src, dst, label in edges:
        G.add_edge(src, dst, label=label)

    A = to_agraph(G)
    A.graph_attr.update(rankdir="LR", splines="curved",
                        label="Financial Automation Pipeline",
                        fontsize="16", labelloc="t", bgcolor="white")
    A.layout("dot")
    A.draw(output_path, format="png")
    print(f"✅ Written: {output_path}")
