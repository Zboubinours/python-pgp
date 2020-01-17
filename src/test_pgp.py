import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from src.user import *


class TestPgp:
    def test_signing(self):
        user = User()

        msg = b'Sign this please.'
        signed_hash = user.sign_message(msg)
        assert user.verify_message(msg, signed_hash, user.public_key) is True

    def test_aes_encrypt(self):
        key = os.urandom(32)
        iv = os.urandom(16)
        msg = b"This is a secret message"

        user = User()
        encrypted_msg = user.encrypt(msg, key, iv)
        decrypted_msg = user.decrypt(encrypted_msg, iv, key)

        assert msg == decrypted_msg

    def test_sending_pgp_key(self):
        user = User()
        key = b'here is my pgp key'
        pgp_msg = user.send_pgp_key(key.decode('utf-8'), user.public_key)
        decrypted_msg = user.receive_pgp_key(pgp_msg, user.public_key)
        assert decrypted_msg == key
