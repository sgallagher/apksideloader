import os
import pathlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class MissingAdbKeysError(Exception):
    pass


class KeyValidationError(Exception):
    pass


def validate_keypair(path=pathlib.Path.home() / ".android"):
    path = pathlib.Path(path)

    # First, just test that they exist at all
    try:
        privkey_path = (path / "adbkey").resolve(strict=True)
        pubkey_path = (path / "adbkey.pub").resolve(strict=True)
    except FileNotFoundError:
        raise MissingAdbKeysError("Missing keys")

    # Attempt to load the existing keys
    try:
        with privkey_path.open("rb") as pem_in:
            serialization.load_pem_private_key(pem_in.read(), None, default_backend())
    except ValueError as e:
        raise KeyValidationError("Invalid private key: {}".format(privkey_path)) from e

    try:
        with pubkey_path.open("rb") as pem_in:
            serialization.load_pem_public_key(pem_in.read(), default_backend())
    except ValueError as e:
        raise KeyValidationError("Invalid public key: {}".format(pubkey_path)) from e


def generate_keypair(path=pathlib.Path.home() / ".android"):
    path = pathlib.Path(path)

    # generate private/public key pair
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

    # get public key in OpenSSH format
    public_key = key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # get private key in PEM container format
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Create the path if needed
    path.mkdir(parents=False, exist_ok=True)

    old_umask = os.umask(0o377)
    with (path / "adbkey").open("wb") as pem_out:
        pem_out.write(private_key)

    os.umask(0o333)
    with (path / "adbkey.pub").open("wb") as pem_out:
        pem_out.write(public_key)
    os.umask(old_umask)
