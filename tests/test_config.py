"""Config tests: provider switching must actually switch (regression)."""

import json
from pathlib import Path

import fixbrief.config as cfg


def _isolate(monkeypatch, tmp_path: Path) -> None:
    home = tmp_path / "home"
    monkeypatch.setattr(cfg, "HOME_DIR", home)
    monkeypatch.setattr(cfg, "CONFIG_PATH", home / ".openminion" / "agents.json")
    monkeypatch.setattr(cfg, "DATA_ROOT", home / "data")


def test_provider_switch_overwrites_config(monkeypatch, tmp_path):
    _isolate(monkeypatch, tmp_path)
    cfg.ensure_config("echo")
    provider, _ = cfg.active_provider_model()
    assert provider == "echo"

    cfg.ensure_config("openai", "gpt-4.1-mini")
    provider, model = cfg.active_provider_model()
    assert provider == "openai"
    assert model == "gpt-4.1-mini"

    # Same-provider re-ensure only patches the model.
    cfg.ensure_config("openai", "gpt-4.1")
    provider, model = cfg.active_provider_model()
    assert (provider, model) == ("openai", "gpt-4.1")


def test_base_url_override(monkeypatch, tmp_path):
    _isolate(monkeypatch, tmp_path)
    monkeypatch.setenv("FIXBRIEF_BASE_URL", "http://127.0.0.1:8000/v1")
    monkeypatch.setenv("FIXBRIEF_API_KEY", "local")
    path = cfg.ensure_config("openai", "local-model")
    data = json.loads(path.read_text(encoding="utf-8"))
    entry = data["providers"]["openai"]
    assert entry["base_url"] == "http://127.0.0.1:8000/v1"
    assert entry["api_key"] == "local"
    assert entry["model"] == "local-model"
