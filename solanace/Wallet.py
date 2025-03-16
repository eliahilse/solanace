from __future__ import annotations
from typing import Union
import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey


class Wallet:
    """Manage Solana Wallets"""
    def __init__(self, private_key: bytes):
        self.kp = Keypair.from_bytes(private_key)

    @classmethod
    def from_private_key(cls, private_key: Union[bytes, str]) -> Wallet:
        """Create a wallet from a private key (base58 or as bytes)"""
        if isinstance(private_key, str):
            private_key = base58.b58decode(private_key)

        elif isinstance(private_key, bytes):
            pass

        else:
            raise TypeError("private_key must be either bytes or str")

        return cls(bytearray(private_key))

    def address(self) -> str:
        """Returns the wallet's address"""
        return str(self.kp.pubkey())
