# diagram-ctl
> Programmatic ecosystem diagrams — built on [diagrammer-x](https://github.com/k4rlski/diagrammer-x)

Generates visual diagrams of the auto-ctl tool ecosystem from structured JSON data.

## Install
```bash
sudo apt install graphviz
git clone git@github.com:k4rlski/diagram-ctl.git /opt/auto-cmd/diagram-ctl
cd /opt/auto-cmd/diagram-ctl
python3 -m venv venv && source venv/bin/activate
pip install networkx pygraphviz
pip install -e .
```

## Usage
```bash
diagram-ctl category   # Tools by category
diagram-ctl server     # Tools by server
diagram-ctl pipeline   # Financial pipeline
diagram-ctl all        # All three → output/
```

## Update the Diagram
Edit `data/auto-ctl-ecosystem.json` → re-run. No code changes needed.

## Engine
Uses the same NetworkX + PyGraphviz stack as [diagrammer-x](https://github.com/k4rlski/diagrammer-x).
