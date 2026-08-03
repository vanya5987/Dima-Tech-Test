import hashlib
import hmac

class WebhookEmulator:
    @staticmethod
    def build_signature(account_id, amount, transaction_id, user_id, secret_key: str) -> str:
        raw: str = f"{account_id}{amount}{transaction_id}{user_id}{secret_key}"

        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def is_signature_valid(account_id: int, amount, transaction_id: str,
                           user_id: int, signature: str, secret_key: str) -> bool:
        expected: str = WebhookEmulator.build_signature(account_id, amount, transaction_id, user_id, secret_key)

        return hmac.compare_digest(expected, signature)