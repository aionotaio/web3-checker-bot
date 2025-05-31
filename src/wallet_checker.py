from typing import Any

import aiohttp
import pyuseragents

from src.vars import TOKENS_PER_NODE_0G


class WalletChecker:
    def __init__(self, wallet_address: str) -> None:
        self.wallet_address = wallet_address
        self.user_agent = pyuseragents.random()

    def format_address(self, visible_chars: int = 4) -> str:
        return f'{self.wallet_address[:visible_chars]}...{self.wallet_address[-visible_chars:]}'
    
    async def get_sophon_allocation(self) -> int:
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://claim.sophon.xyz',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://claim.sophon.xyz',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-api-key': 'MG9788WsRg0TLyGnKMphIr'
        }

        params = {
            'id': self.wallet_address,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.claim.sophon.xyz/eligibility', params=params, headers=headers) as response:
                if response.status == 200:
                    result_dict: dict[str, Any] = await response.json()
                    allocation_array: list[dict[str, Any]] = result_dict.get('allocations', [])
                    if len(allocation_array) == 0:
                        return 0
                    return int(allocation_array[0].get('tokenAmount', 0)) // 10 ** 18
                return 0
        
    async def get_sxt_allocation(self) -> int: 
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://gigaclaim.spaceandtime.io/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent
        }

        params = {
            'address': self.wallet_address
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get('https://gigaclaim.spaceandtime.io/api/proof', params=params, headers=headers) as response:
                if response.status == 200:
                    result_dict: dict[str, Any] = await response.json()
                    return int(result_dict.get('amount', 0)) // 10 ** 18
                return 0

    async def get_0g_allocation(self) -> int: 
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://claim.0gfoundation.ai',
            'Pragma': 'no-cache',
            'Referer': 'https://claim.0gfoundation.ai/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': self.user_agent,
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        body = f"""
            {{"jsonrpc":"2.0","method":"getNFTClaims","params":{{"account":"{self.wallet_address}"}},"id":1}}
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.post('https://rebate-commission-airdrop.0g.ai/airdrop', data=body, headers=headers) as response:
                if response.status == 200:
                    result_dict: dict[str, Any] = await response.json()
                    return int(result_dict.get('result', {}).get('totalNodes', 0)) * TOKENS_PER_NODE_0G
                return 0

    async def get_jager_eligibility(self) -> bool: 
        headers = {
            'accept': 'application/json',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'Bearer undefined',
            'cache-control': 'no-cache',
            'origin': 'https://jager.meme',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://jager.meme/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.jager.meme/api/airdrop/queryAirdrop/{self.wallet_address}', headers=headers) as response:
                if response.status == 200:
                    result_dict: dict[str, Any] = await response.json()
                    return bool(result_dict.get('data', {}).get('canAirdrop', False))
                return False
