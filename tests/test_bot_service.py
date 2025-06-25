import pytest
from mongomock_motor import AsyncMongoMockClient

from shared.bot_service import BotService
from shared.schemas import BotUser, BotUserUpdateData

from shared.exceptions import AlreadyExistsError, MissingError
from tests.mocks.fixtures import get_samples_for_service, get_data, SAMPLE_WALLET


collection = AsyncMongoMockClient()['tests']['test-1']
bot_service = BotService(collection)


@pytest.mark.asyncio
async def test_create_one_user(get_samples_for_service: list[BotUser]) -> None:
    for sample in get_samples_for_service:
        result = await bot_service.create_one_user(sample)
        assert result == sample
    
    with pytest.raises(AlreadyExistsError):
        await bot_service.create_one_user(get_samples_for_service[2])


@pytest.mark.asyncio
async def test_create_one_wallet() -> None:
    result_1 = await bot_service.create_one_wallet(3, SAMPLE_WALLET)
    assert result_1 != None

    with pytest.raises(MissingError):
        await bot_service.create_one_wallet(123456, SAMPLE_WALLET)


@pytest.mark.asyncio 
async def test_read_one_user(get_samples_for_service: list[BotUser]) -> None:
    result_1 = await bot_service.read_one_user(4)
    assert result_1 == get_samples_for_service[3]

    with pytest.raises(MissingError):
        await bot_service.read_one_user(123456)


@pytest.mark.asyncio     
async def test_read_one_wallet() -> None:
    result_1 = await bot_service.read_one_wallet(3, SAMPLE_WALLET)
    assert result_1 != None

    with pytest.raises(MissingError):
        await bot_service.read_one_wallet(3, "not_existing_wallet")

    with pytest.raises(MissingError):
        await bot_service.read_one_wallet(123456, SAMPLE_WALLET)

    with pytest.raises(MissingError):
        await bot_service.read_one_wallet(123456, "not_existing_wallet")


@pytest.mark.asyncio  
async def test_read_all_wallets() -> None:
    result_1 = await bot_service.read_all_wallets(3)
    assert result_1 != None

    with pytest.raises(MissingError):
        await bot_service.read_all_wallets(123456)  


@pytest.mark.asyncio   
async def test_update_one_user(get_data: BotUserUpdateData) -> None:
    result_1 = await bot_service.update_one_user(3, get_data)
    assert result_1 == None

    with pytest.raises(MissingError):
        await bot_service.update_one_user(123456, get_data)
    

@pytest.mark.asyncio               
async def test_delete_one_wallet() -> None:
    result_1 = await bot_service.delete_one_wallet(3, SAMPLE_WALLET)
    assert result_1 != None

    with pytest.raises(MissingError):
        await bot_service.delete_one_wallet(3, "not_existing_wallet")

    with pytest.raises(MissingError):
        await bot_service.delete_one_wallet(123456, SAMPLE_WALLET)

    with pytest.raises(MissingError):
        await bot_service.delete_one_wallet(123456, "not_existing_wallet")


@pytest.mark.asyncio   
async def test_delete_all_wallets(get_samples_for_service: list[BotUser]) -> None:
    sample_dict = get_samples_for_service[3].model_dump()
    sample_dict["wallets"] = []

    sample_user_4 = BotUser.model_validate(sample_dict)

    result_1 = await bot_service.delete_all_wallets(4)
    assert result_1 == sample_user_4
