import json
from pathlib import Path

import pytest

from weather_cli.main import fetch_weather


def test_fetch_weather(monkeypatch):
    sample_json = {
        "current_condition": [
            {
                "temp_C": "25",
                "weatherDesc": [{"value": "Sunny"}],
            }
        ]
    }

    class DummyResp:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return sample_json

    def dummy_get(url, timeout=10):  # noqa: D401
        return DummyResp()

    monkeypatch.setattr("requests.get", dummy_get)

    result = fetch_weather("Tokyo")
    assert result == {"temp_C": "25", "description": "Sunny"} 