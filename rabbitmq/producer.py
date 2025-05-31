from rabbitmq_rpc import RPCClient

from src.wallet_checker import WalletChecker


class Producer:
    def __init__(self, wallet_address: str, rpc_client: RPCClient):
        self.rpc_client = rpc_client
        self.wallet_address = wallet_address
        self.wallet_checker = WalletChecker(wallet_address)

    async def publish_events(self, projects: list[str], uuid: str):
        for project in projects:
            if project == 'sophon':
                await self.rpc_client.register_event(f'sophon_{uuid}', self.wallet_checker.get_sophon_allocation)
            elif project == 'sxt':
                await self.rpc_client.register_event(f'sxt_{uuid}', self.wallet_checker.get_sxt_allocation)
            elif project == '0g':
                await self.rpc_client.register_event(f'0g_{uuid}', self.wallet_checker.get_0g_allocation)
            elif project == 'jager':
                await self.rpc_client.register_event(f'jager_{uuid}', self.wallet_checker.get_jager_eligibility)
