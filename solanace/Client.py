from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey

from solana.rpc.api import Client
from solana.transaction import Transaction
import json
from functools import partial

class Client:
    """Synchronous client implementation, fully gevent compatible."""
    def __init__(self, **client_urls: str):
        self.clients = [Client(client_url) for client_url in client_urls]

    def _client_request(self, func):
        """Attempt a sync request across all clients until successful."""
        for client in self.clients:
            try:
                response = func(client)
                return response
            except Exception as e:
                print(f"Failed to process sync request with client. Error: {e}")

        raise Exception("All sync client requests failed.")

    def get_token_balance(self, wallet_address: str, token_mint_address: str) -> float:

        opts = TokenAccountOpts(mint=Pubkey.from_string(token_mint_address))

        func_partial = partial(
                lambda client,
                pubkey,
                opts: client.get_token_accounts_by_owner_json_parsed(pubkey, opts).to_json(),
                pubkey=Pubkey.from_string(wallet_address),
                opts=opts)

        associated_token_accounts_json = self._client_request(func_partial)

        associated_token_accounts = json.loads(associated_token_accounts_json)

        total_token_balance = 0

        for token_account in associated_token_accounts["result"]["value"]:

            balance = int(token_account["account"]["data"]["parsed"]["info"]["tokenAmount"]["amount"])
            decimals = int(token_account["account"]["data"]["parsed"]["info"]["tokenAmount"]["decimals"])

            balance_in_token = balance * (10 ** -decimals)
            total_token_balance += balance_in_token

        return total_token_balance

