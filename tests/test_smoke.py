"""Smoke tests: prove the schema loads and the generated Python data
models import cleanly. Existing primarily so `just test` has at least
one collected pytest item (pytest exits with code 5 — failure — when
zero tests are collected, which would otherwise block CI).

When real example data lands under `tests/data/{valid,invalid}/`, the
`linkml-run-examples` step in `just _test-examples` will exercise the
schema end-to-end and these smoke checks become a thin safety net.
"""

from pathlib import Path

SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "core_person"
    / "schema"
    / "core_person.yaml"
)


def test_schema_file_exists():
    assert SCHEMA_PATH.is_file(), f"schema not found at {SCHEMA_PATH}"


def test_schema_loads_via_linkml_runtime():
    from linkml_runtime.utils.schemaview import SchemaView

    sv = SchemaView(str(SCHEMA_PATH))
    classes = sv.all_classes()
    # The 9 entity classes documented in CLAUDE.md.
    expected = {
        "Person",
        "Identifier",
        "Address",
        "ContactPoint",
        "Agent",
        "Jurisdiction",
        "Location",
        "Document",
        "Concept",
    }
    missing = expected - set(classes)
    assert not missing, f"expected classes missing from schema: {sorted(missing)}"


def test_generated_pydantic_imports():
    from core_person.datamodel import core_person_pydantic as m

    person = m.Person()
    assert person is not None
