from datetime import datetime, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from shared.schemas import BotUser
from shared.exceptions import MissingError
from shared.bot_instance import BotInstance
from admin.services.admin_service import AdminService

from tests.mocks.fixtures import get_samples_for_service


collection = AsyncMongoMockClient()["tests"]["test-1"]
admin_service = AdminService(collection)


@pytest.mark.asyncio
async def test_create_one_user(get_samples_for_service: list[BotUser]) -> None:
    for sample in get_samples_for_service:
        result = await admin_service.create_one_user(sample)
        assert result == sample


@pytest.mark.asyncio
async def test_read_all_users(get_samples_for_service: list[BotUser]) -> None:
    # Все пользователи без фильтрации
    result_1 = await admin_service.read_all_users()
    assert result_1 == get_samples_for_service

    # Все пользователи по одному фильтру
    result_2 = await admin_service.read_all_users(language_code="ru")
    assert result_2 == [
        user for user in get_samples_for_service if user.language_code == "ru"
    ]

    # Полная пагинация
    result_3 = await admin_service.read_all_users(page=0, size=1)
    assert result_3 == [get_samples_for_service[0]]

    # Неполная пагинация
    result_4 = await admin_service.read_all_users(size=5)
    assert result_4 == get_samples_for_service

    result_5 = await admin_service.read_all_users(page=5)
    assert result_5 == get_samples_for_service

    # Полная пагинация вместе с фильтрацией
    result_6 = await admin_service.read_all_users(page=0, size=1, language_code="ru")
    assert result_6 == [get_samples_for_service[37]]

    # Полная пагинация при выходе за диапазон
    result_7 = await admin_service.read_all_users(page=999, size=99)
    assert result_7 == []


@pytest.mark.asyncio
async def test_ban_one_user() -> None:
    with pytest.raises(MissingError):
        await admin_service.ban_one_user(999999)

    result_1 = await admin_service.ban_one_user(1)
    true_result_1 = await admin_service.read_one_user(1)
    assert true_result_1 == result_1

    result_2 = await admin_service.ban_one_user(2)
    true_result_2 = await admin_service.read_one_user(2)
    assert result_2 == true_result_2


@pytest.mark.asyncio
async def test_unban_one_user() -> None:
    with pytest.raises(MissingError):
        await admin_service.unban_one_user(999999)

    result_1 = await admin_service.unban_one_user(1)
    true_result_1 = await admin_service.read_one_user(1)
    assert result_1 == true_result_1

    result_2 = await admin_service.unban_one_user(2)
    true_result_2 = await admin_service.read_one_user(2)
    assert result_2 == true_result_2


@pytest.mark.asyncio
async def test_send_message_to_one_user() -> None:
    with pytest.raises(MissingError):
        await admin_service.send_message_to_one_user(
            999999, BotInstance.get_bot(), "Hello World!"
        )


@pytest.mark.asyncio
async def test_get_active_stats(get_samples_for_service: list[BotUser]) -> None:
    result_1 = await admin_service.get_active_stats(
        get_samples_for_service, datetime.now(timezone.utc)
    )
    assert result_1 != None


@pytest.mark.asyncio
async def test_get_language_stats(get_samples_for_service: list[BotUser]) -> None:
    result_1 = await admin_service.get_language_stats(get_samples_for_service)
    assert result_1 != None


@pytest.mark.asyncio
async def get_all_stats(get_samples_for_service: list[BotUser]) -> None:
    result_1 = await admin_service.get_all_stats(
        get_samples_for_service, datetime.now(timezone.utc)
    )
    assert result_1 != None
