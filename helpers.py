def get_headers(token: str, custom_headers: dict = None) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    if custom_headers:
        headers.update(custom_headers)
    return headers
