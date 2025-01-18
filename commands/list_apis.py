import typer
import requests
from config import validate_config
from helpers import get_headers

def list_all_apis():
    """List all APIs using the configured URL and Bearer Token."""
    api_url, token = validate_config()
    next_page_url = f"{api_url}/management/v2/environments/DEFAULT/apis/?page=1&size=10"

    try:
        while next_page_url:
            headers = get_headers(token)
            response = requests.get(next_page_url, headers=headers)

            if response.ok:
                apis = response.json()
                for api in apis.get("data", []):
                    typer.echo(f"ID: {api['id']}, Name: {api['name']}")
                next_page_url = apis.get("links", {}).get("next", None)
            else:
                typer.echo(f"Error: {response.status_code} - {response.text}")
                break
    except requests.RequestException as e:
        typer.echo(f"An error occurred: {str(e)}")
