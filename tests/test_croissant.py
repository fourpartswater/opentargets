from opentargets import croissant_introspect as ci

def test_sample_manifest_parsing():
    cols, pks, fks = ci.parse_structure(ci.SAMPLE_MANIFEST)
    assert len(cols) == 3
    assert pks == ["evidence_id"]
    assert ("target_id", "target", "id") in fks


def test_fetch_manifest_offline():
    mani = ci.fetch_manifest("whatever", offline=True)
    assert mani == ci.SAMPLE_MANIFEST


def test_list_datasets_fallback(monkeypatch):
    def boom(url, timeout=10):
        raise RuntimeError("no net")

    monkeypatch.setattr(ci.urllib.request, "urlopen", boom)
    datasets = ci.list_datasets()
    assert datasets == ci.SAMPLE_DATASETS


def test_cli_list(capsys):
    ci.main(["--list", "--offline"])
    out = capsys.readouterr().out.splitlines()
    assert set(out) == set(ci.SAMPLE_DATASETS)
