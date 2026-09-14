from anancapital import pst


def test_update_with_config_passes_yaml_session(monkeypatch):
    config = {
        "barchart_username": "test-user",
        "barchart_password": "test-password",
        "barchart_update_list": ["GOLD", "AUD"],
        "barchart_path": "/tmp/test-prices",
        "barchart_dry_run": True,
    }
    expected_session = object()
    calls = []

    monkeypatch.setattr(pst, "load_config", lambda _path: config)
    monkeypatch.setattr(pst, "create_bc_session", lambda _config: expected_session)
    monkeypatch.setattr(
        pst,
        "update_barchart_downloads",
        lambda **kwargs: calls.append(kwargs),
    )

    pst.update_with_config()

    assert [call["instr_code"] for call in calls] == ["GOLD", "AUD"]
    assert all(call["session"] is expected_session for call in calls)
    assert all(call["save_dir"] == "/tmp/test-prices" for call in calls)
    assert all(call["dry_run"] is True for call in calls)
