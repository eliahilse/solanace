# solanace
A high-level Python library to effortlessly interact with the Solana Blockchain (work in progress).

### Features
- Simplistic syntax
- Full support for Asyncio & Gevent (but can also run synchronous)
- Fallback clients
- Swapping functionality using Jupiter Aggregator (raydium, orca, etc.)
- High performance (uses solders, written in Rust, under the hood)
- Meaningful error messages
- RPC Performance Testing & Profiling
- Full support for Type Hints

For support, drop me a DM on my [X](https://x.com/eliahilse).

_Following is the goal, this library is WIP_
### Get Started

```python
from solanace import Tokens, Metrics
from solanace import Wallet, Client

my_wallet = Wallet.from_private_key("xyzxyzxyz")  # base58 encoded private key
my_client = Client("https://sola.na/rpc", "https://mainnet-beta.solana.com/rpc")

# send and recieve solana & spl tokens
my_client.get_balance()
my_client.send_sol(wallet=my_wallet, to="bob.sol", amount=0.1)
my_client.send_token(wallet=my_wallet, token=Tokens.USDC, to="bob.sol", amount=2)
my_wallet_address = my_wallet.address()

# swap 0.1 solana to usdc
my_client.swap(wallet=my_wallet, from_currency=Tokens.Solana, to_currency=Tokens.USDC, amount_from_currency=0.1)
my_client.swap(wallet=my_wallet, from_currency=Tokens.Solana, to_currency=Tokens.USDC, amount_to_currency=5)

# nft utility
my_client.send_nft(wallet=my_wallet, nft_address="xyz", to="abc")
my_client.burn_nft(wallet=my_wallet, nft_address="uvw")

# test rpcs
Metrics.test(urls=["rpc1", "rpc2", "rpc3"], limit=10)
```

### Upcoming Features
- Mint NFTs
- Mint Tokens
- List, Buy & Bid on NFTs
- Whitelist Wallets & Limit amounts sent
