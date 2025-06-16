import uuid


def generate_key(username: str) -> str:
    try:
        secret_key = uuid.uuid4().hex
        return secret_key + username
    except Exception as e:
        raise RuntimeError(f"Failed to generate key: {str(e)}")
