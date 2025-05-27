import unittest
import base58
from solders.keypair import Keypair
from solanace.Wallet import Wallet


class TestWallet(unittest.TestCase):
    def setUp(self):
        """Generate a random keypair for testing"""
        self.keypair = Keypair()
        self.private_key_bytes = self.keypair.to_bytes()
        self.private_key_b58 = base58.b58encode(self.private_key_bytes).decode('utf-8')

    def test_create_wallet_from_valid_private_key_bytes(self):
        """Test creating a wallet from valid private key bytes"""
        wallet = Wallet.from_private_key(self.private_key_bytes)
        self.assertEqual(wallet.address(), str(self.keypair.pubkey()))

    def test_create_wallet_from_valid_base58_private_key(self):
        """Test creating a wallet from valid base58 encoded private key"""
        wallet = Wallet.from_private_key(self.private_key_b58)
        self.assertEqual(wallet.address(), str(self.keypair.pubkey()))

    def test_create_wallet_accepts_private_key_bytes(self):
        """Test wallet creation accepts private key bytes"""
        wallet = Wallet.from_private_key(self.private_key_bytes)
        self.assertIsInstance(wallet, Wallet)

    def test_create_wallet_accepts_base58_private_key_string(self):
        """Test wallet creation accepts base58 string private key"""
        wallet = Wallet.from_private_key(self.private_key_b58)
        self.assertIsInstance(wallet, Wallet)

    def test_create_wallet_with_invalid_private_key_type_raises(self):
        """Test that invalid private key type raises TypeError"""
        with self.assertRaises(TypeError):
            Wallet.from_private_key(112233455)


if __name__ == '__main__':
    unittest.main()
