import uuid


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def isValid_link(username: str, address: str, port: int) -> bool:
    if is_valid_uuid(username):
        return True

    return False
