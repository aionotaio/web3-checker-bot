import json
from typing import Any

import pytest

from shared.vars import MOCK_DB_PATH
from shared.schemas import BotUserUpdateData, BotUser


SAMPLE_WALLET: str = '0x5F28179797e5939E22D66aabc7027f3D3114B59b'


@pytest.fixture()
def get_samples_for_repo() -> list[dict[str, Any]]:
    with open(MOCK_DB_PATH) as f:
        return json.load(f)


@pytest.fixture()
def get_samples_for_service() -> list[BotUser]:
    with open(MOCK_DB_PATH) as f:
        arr = json.load(f)
    return [BotUser.model_validate(user) for user in arr]


@pytest.fixture()
def get_data() -> BotUserUpdateData:
    user_data = {
        "full_name": "Pooh Rummings",
        "username": "prummings3",
        "is_premium": False,
        "language_code": "ru",
        "last_active_at": "2025-05-28 19:21:09",
    }
    return BotUserUpdateData.model_validate(user_data)
