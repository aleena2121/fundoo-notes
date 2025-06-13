import uuid


def generate_key(name: str) -> str:
    secret_key = uuid.uuid4().hex
    return secret_key + name
