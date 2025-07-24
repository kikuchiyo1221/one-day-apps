#!/usr/bin/env python3
"""weather_cli

Usage::

    python main.py --city Tokyo

取得元: wttr.in (キー不要) - https://wttr.in/<CITY>?format=j1
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

import requests

API_TEMPLATE = "https://wttr.in/{city}?format=j1"


def fetch_weather(city: str) -> Dict[str, Any]:
    """指定都市の天気情報を取得して辞書を返す。

    返却例::
        {
            "temp_C": "27",
            "description": "Partly cloudy"
        }
    """
    url = API_TEMPLATE.format(city=city)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    try:
        current = data["current_condition"][0]
        return {
            "temp_C": current["temp_C"],
            "description": current["weatherDesc"][0]["value"],
        }
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected API response") from None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple Weather CLI (wttr.in)")
    parser.add_argument("--city", required=True, help="City name (e.g., Tokyo)")
    return parser


def main(argv: list[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    args = build_parser().parse_args(argv)

    try:
        weather = fetch_weather(args.city)
        print(f"{args.city}: {weather['temp_C']}°C, {weather['description']}")
    except Exception as exc:
        print("Error:", exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 