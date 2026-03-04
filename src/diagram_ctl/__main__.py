#!/usr/bin/env python3
"""
diagram-ctl — programmatic ecosystem diagrams
Usage:
  diagram-ctl category   [--data DATA] [--out OUTPUT]
  diagram-ctl server     [--data DATA] [--out OUTPUT]
  diagram-ctl pipeline   [--data DATA] [--out OUTPUT]
  diagram-ctl all        [--data DATA] [--outdir OUTDIR]
"""
import argparse, sys
from pathlib import Path
from .renderer import load_ecosystem, render_by_category, render_by_server, render_pipeline

DEFAULT_DATA = Path(__file__).parent.parent.parent / "data" / "auto-ctl-ecosystem.json"
DEFAULT_OUT  = Path("output")


def main():
    parser = argparse.ArgumentParser(prog="diagram-ctl")
    sub = parser.add_subparsers(dest="cmd")

    for name in ["category", "server", "pipeline"]:
        p = sub.add_parser(name)
        p.add_argument("--data", default=str(DEFAULT_DATA))
        p.add_argument("--out", default=f"output/diagram-ctl-{name}.png")

    p_all = sub.add_parser("all")
    p_all.add_argument("--data", default=str(DEFAULT_DATA))
    p_all.add_argument("--outdir", default="output")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    if args.cmd == "all":
        data = load_ecosystem(args.data)
        out = Path(args.outdir)
        out.mkdir(exist_ok=True)
        render_by_category(data, str(out / "ecosystem-by-category.png"))
        render_by_server(data,   str(out / "ecosystem-by-server.png"))
        render_pipeline(data,    str(out / "financial-pipeline.png"))
    else:
        data = load_ecosystem(args.data)
        Path(args.out).parent.mkdir(exist_ok=True)
        fn = {"category": render_by_category, "server": render_by_server, "pipeline": render_pipeline}[args.cmd]
        fn(data, args.out)


if __name__ == "__main__":
    main()
