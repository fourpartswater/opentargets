import croissant_introspect as ci

def test_sample_manifest_parsing():
    cols, pks, fks = ci.parse_structure(ci.SAMPLE_MANIFEST)
    assert len(cols) == 3
    assert pks == ["evidence_id"]
    assert ("target_id", "target", "id") in fks
