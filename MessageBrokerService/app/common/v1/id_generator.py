from uuid import uuid1

def generate_primary_id(_prefix: str = "service") -> str:
    return f"{_prefix}{uuid1().hex}"