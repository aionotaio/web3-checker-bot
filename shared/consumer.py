from typing import Any

from rabbitmq_rpc import RPCClient

from shared.wallet_checker import WalletChecker


class Consumer:
    def __init__(self, wallet_address: str, rpc_client: RPCClient):
        self.rpc_client = rpc_client
        self.wallet_address = wallet_address
        self.wallet_checker = WalletChecker(wallet_address)

    async def consume_events(self, projects: list[str], uuid: str) -> dict[str, Any]:
        wallet_results: dict[str, Any] = {}

        for project in projects:
            result = await self.rpc_client.call(f'{project}_{uuid}', {})
            wallet_results[project] = result
        
        await self.rpc_client.reconnect()
        
        return wallet_results
