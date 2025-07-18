TOKEN_DENYLIST: set = set()

def add_token_to_denylist(jti: str):
    TOKEN_DENYLIST.add(jti)
    print(f"Token {jti} adicionado à denylist.")

def is_token_denied(jti: str) -> bool:
    return jti in TOKEN_DENYLIST