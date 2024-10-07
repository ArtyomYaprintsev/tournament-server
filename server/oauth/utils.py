import hashlib
import os
import binascii


def generate_code(length: int = 10):
    return binascii.hexlify(os.urandom(length)).decode("utf-8")


def get_state() -> str:
    return generate_code(32)


class PKCE:
    _code_verifier: str
    code_challenge: str
    code_challenge_method: str = "s256"

    def __init__(self) -> None:
        self._code_verifier = generate_code(length=32)
        self.code_challenge = hashlib.sha256(
            self._code_verifier.encode(),
        ).hexdigest()

    def to_dict(self) -> dict[str, str]:
        return {
            "code_challenge": self.code_challenge,
            "code_challenge_method": self.code_challenge_method,
        }
