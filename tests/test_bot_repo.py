from typing import Any

import pytest
from mongomock_motor import AsyncMongoMockClient

from shared.bot_repo import BotRepository
from shared.schemas import BotUser
from tests.mocks.fixtures import get_samples_for_repo, SAMPLE_WALLET


collection = AsyncMongoMockClient()['tests']['test-1']
bot_repo = BotRepository(collection) 
    
    
@pytest.mark.asyncio
async def test_create_one_user(get_samples_for_repo: list[dict[str, Any]]) -> None:
    for sample in get_samples_for_repo:
        result = await bot_repo.create_one_user(sample)
        assert BotUser.model_validate(result) == BotUser.model_validate(sample)


@pytest.mark.asyncio
async def test_create_one_wallet() -> None:
    result_1 = await bot_repo.create_one_wallet(1, SAMPLE_WALLET)
    assert result_1 != None

    result_2 = await bot_repo.create_one_wallet(123456, SAMPLE_WALLET)
    assert result_2 == None


@pytest.mark.asyncio    
async def test_read_one_user(get_samples_for_repo: list[dict[str, Any]]) -> None:
    result_1 = await bot_repo.read_one_user(2)
    assert BotUser.model_validate(result_1) == BotUser.model_validate(get_samples_for_repo[1])

    result_2 = await bot_repo.read_one_user(123456)
    assert result_2 == None


@pytest.mark.asyncio 
async def test_read_one_wallet() -> None:
    result_1 = await bot_repo.read_one_wallet(1, SAMPLE_WALLET)
    assert result_1 != None

    result_2 = await bot_repo.read_one_wallet(1, "not_existing_wallet")
    assert result_2 == None

    result_3 = await bot_repo.read_one_wallet(123456, SAMPLE_WALLET)
    assert result_3 == None

    result_4 = await bot_repo.read_one_wallet(123456, "not_existing_wallet")
    assert result_4 == None


@pytest.mark.asyncio 
async def test_delete_one_wallet() -> None:
    result_1 = await bot_repo.delete_one_wallet(1, SAMPLE_WALLET)
    assert result_1 != None

    result_2 = await bot_repo.delete_one_wallet(1, "not_existing_wallet")
    assert result_2 == None

    result_3 = await bot_repo.delete_one_wallet(123456, SAMPLE_WALLET)
    assert result_3 == None

    result_4 = await bot_repo.delete_one_wallet(123456, "not_existing_wallet")
    assert result_4 == None


@pytest.mark.asyncio 
async def test_delete_all_wallets(get_samples_for_repo: list[dict[str, Any]]) -> None:
    get_samples_for_repo[0]["wallets"] = []

    result_1 = await bot_repo.delete_all_wallets(1)
    assert BotUser.model_validate(result_1) == BotUser.model_validate(get_samples_for_repo[0])
