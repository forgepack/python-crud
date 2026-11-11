import os

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("DATABASE_SCHEMA", "main")

_KINDS = ("unit", "integration", "e2e")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Aplica o marker (unit/integration/e2e) conforme a pasta do teste."""
    for item in items:
        for kind in _KINDS:
            if kind in item.path.parts:
                item.add_marker(getattr(pytest.mark, kind))
