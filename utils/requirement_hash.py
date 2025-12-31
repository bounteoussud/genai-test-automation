import hashlib

def get_requirement_hash(text: str) -> str:
    return hashlib.md5(text.strip().encode("utf-8")).hexdigest()
