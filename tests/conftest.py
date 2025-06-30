"""
Pytest configuration and fixtures
"""

import asyncio
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from server.storage.tide_storage import TideStorage


@pytest.fixture(scope="function")
def temp_storage_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for storage testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def tide_storage(temp_storage_dir: Path) -> TideStorage:
    """Create a TideStorage instance with temporary directory"""
    return TideStorage(str(temp_storage_dir))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
