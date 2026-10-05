from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import yaml

from scripts.keep_space_awake import keep_awake, main

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "restart-space.yml"
EXPECTED_SPACES = {"ferferefer/Glaucoma-EyeFundus-ML", "ferferefer/retinal_age"}


def fake_api(stage):
    api = MagicMock()
    api.get_space_runtime.return_value = SimpleNamespace(stage=stage)
    return api


@pytest.mark.parametrize("space", sorted(EXPECTED_SPACES))
@pytest.mark.parametrize("stage", ["RUNNING", "BUILDING", "APP_STARTING", "RUNNING_APP_STARTING"])
def test_healthy_space_is_not_restarted(space, stage):
    api = fake_api(stage)

    assert keep_awake(api, space) == 0
    api.get_space_runtime.assert_called_once_with(space)
    api.restart_space.assert_not_called()


@pytest.mark.parametrize("space", sorted(EXPECTED_SPACES))
@pytest.mark.parametrize("stage", ["SLEEPING", "PAUSED", "RUNTIME_ERROR", "STOPPED"])
def test_sleeping_or_broken_space_is_restarted(space, stage):
    api = fake_api(stage)

    assert keep_awake(api, space) == 0
    api.restart_space.assert_called_once_with(repo_id=space)


def test_runtime_query_failure_returns_error():
    api = MagicMock()
    api.get_space_runtime.side_effect = RuntimeError("boom")

    assert keep_awake(api, "ferferefer/retinal_age") == 1
    api.restart_space.assert_not_called()


def test_restart_failure_returns_error():
    api = fake_api("SLEEPING")
    api.restart_space.side_effect = RuntimeError("boom")

    assert keep_awake(api, "ferferefer/retinal_age") == 1


def test_main_requires_token(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    monkeypatch.setenv("SPACE_ID", "ferferefer/retinal_age")

    assert main() == 1


def test_main_requires_space_id(monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "hf_x")
    monkeypatch.delenv("SPACE_ID", raising=False)

    assert main() == 1


def test_workflow_watches_both_spaces_with_the_script():
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    job = workflow["jobs"]["restart-space"]

    assert set(job["strategy"]["matrix"]["space"]) == EXPECTED_SPACES
    assert job["strategy"]["fail-fast"] is False

    steps = job["steps"]
    assert any(s.get("uses", "").startswith("actions/checkout") for s in steps)
    run_step = next(s for s in steps if "keep_space_awake.py" in s.get("run", ""))
    assert run_step["env"]["SPACE_ID"] == "${{ matrix.space }}"
    assert run_step["env"]["HF_TOKEN"] == "${{ secrets.HF_TOKEN }}"
