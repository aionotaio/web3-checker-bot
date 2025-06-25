from rabbitmq_rpc import RPCClient

from shared.wallet_checker import WalletChecker


class Producer:
    def __init__(self, wallet_address: str, rpc_client: RPCClient) -> None:
        self.rpc_client = rpc_client
        self.wallet_address = wallet_address
        self.wallet_checker = WalletChecker(wallet_address)

    async def publish_events(self, projects: list[str], uuid: str) -> None:
        for project in projects:
            if project == "sophon":
                await self.rpc_client.register_event(
                    f"sophon_{uuid}",
                    self.wallet_checker.get_sophon_allocation,
                    **{"exclusive": True, "auto_delete": True, "durable": False},
                )
            elif project == "sxt":
                await self.rpc_client.register_event(
                    f"sxt_{uuid}",
                    self.wallet_checker.get_sxt_allocation,
                    **{"exclusive": True, "auto_delete": True, "durable": False},
                )
            elif project == "og":
                await self.rpc_client.register_event(
                    f"og_{uuid}",
                    self.wallet_checker.get_0g_allocation,
                    **{"exclusive": True, "auto_delete": True, "durable": False},
                )
            elif project == "jager":
                await self.rpc_client.register_event(
                    f"jager_{uuid}",
                    self.wallet_checker.get_jager_eligibility,
                    **{"exclusive": True, "auto_delete": True, "durable": False},
                )
