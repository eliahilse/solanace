from solana.rpc import async_api
from solana.transaction import Transaction
from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
import json
from functools import partial
from solanace import Wallet


class AsyncClient:
    """Fully asyncio compatible version, using aiohttp for requests."""
    def __init__(self, log_level: int = 0, **client_urls: str):
        self.clients = [async_api.AsyncClient(client_url) for client_url in client_urls]
        if not isinstance(log_level, int):
            raise Exception("Log Level Invalid")
        self.log_level = log_level

    async def _client_request(self, func):
        """Attempt an async request across all clients until successful."""
        for client in self.clients:
            try:
                response = await func(client)
                return response
            except Exception as e:
                if self.log_level > 1:
                    print(f"Failed to process async request with client {client}. Error: {e}")

        raise Exception("All async client requests failed.")

    async def get_sol_balance(self, wallet: str):
        """Get the solana balance of a wallet"""

        func_partial = partial(
            lambda client, pubkey: client.get_balance(pubkey),
            pubkey=Pubkey.from_string(wallet)
        )
        response = await self._client_request(func_partial)

        return response.value / 1e9

    async def get_token_balance(self, wallet_address: str, token_mint_address: str) -> float:

        opts = TokenAccountOpts(mint=Pubkey.from_string(token_mint_address))

        func_partial = partial(
                lambda client,
                pubkey,
                opts: client.get_token_accounts_by_owner_json_parsed(pubkey, opts).to_json(),
                pubkey=Pubkey.from_string(wallet_address),
                opts=opts)

        associated_token_accounts_json = await self._client_request(func_partial)

        associated_token_accounts = json.loads(associated_token_accounts_json)

        total_token_balance = 0

        for token_account in associated_token_accounts["result"]["value"]:

            balance = int(token_account["account"]["data"]["parsed"]["info"]["tokenAmount"]["amount"])
            decimals = int(token_account["account"]["data"]["parsed"]["info"]["tokenAmount"]["decimals"])

            balance_in_token = balance * (10 ** -decimals)
            total_token_balance += balance_in_token

        return total_token_balance


    async def send_sol(self, wallet: Wallet, recipient_address: str, amount_decimal: float) -> str:
        """Send Solana from the class wallet to a wallet"""

        amount_lamports = int(amount_decimal * 1e9)
        transfer_ix = transfer(
            TransferParams(
                from_pubkey=wallet.kp.pubkey(),
                to_pubkey=Pubkey.from_string(recipient_address),
                lamports=amount_lamports
            )
        )
        transaction = Transaction().add(transfer_ix)
        func_partial = partial(
            lambda client, tx, kp: client.send_transaction(tx, kp),
            tx=transaction,
            kp=wallet.kp
        )

        response = await self._client_request(func_partial)

        return str(response.value)


    async def get_minimum_balance(self, account_size: int = 128) -> float:
        """Returns the minimum amount to stay rent-free (also known as wallet activation fee)"""

        func_partial = partial(
            lambda client, size: client.get_minimum_balance_for_rent_exemption(size),
            size=account_size
        )
        response = await self._client_request(func_partial)
        return response.value / 1e9

    #TODO: Resolve .sol domains to wallet addresses
