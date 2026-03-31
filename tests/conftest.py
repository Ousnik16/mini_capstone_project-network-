import asyncio
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def run_async():
    def runner(coroutine):
        return asyncio.run(coroutine)

    return runner


@pytest.fixture
def payload():
    def make_payload(**values):
        return SimpleNamespace(**values)

    return make_payload


@pytest.fixture
def get_error(run_async):
    def runner(coroutine):
        with pytest.raises(HTTPException) as error:
            run_async(coroutine)
        return error.value

    return runner
