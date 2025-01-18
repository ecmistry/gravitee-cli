import typer
import requests
import logging
from config import validate_config
from helpers import get_headers

logging.basicConfig(level=logging.INFO)

def create_api_payload(name: str, api_version: str, description: str, path: str, target: str) -> dict:
    """Generate the payload for creating an API."""
    return {
        "name": name,
        "apiVersion": api_version,
        "description": description,
        "definitionVersion": "V4",
        "type": "PROXY",
        "listeners": [
            {
                "type": "HTTP",
                "paths": [{"path": path}],
                "entrypoints": [{"type": "http-proxy"}]
            }
        ],
        "endpointGroups": [
            {
                "name": "default-group",
                "type": "http-proxy",
                "endpoints": [
                    {
                        "name": "default",
                        "type": "http-proxy",
                        "weight": 1,
                        "inheritConfiguration": False,
                        "configuration": {"target": target},
                    }
                ]
            }
        ]
    }

def create_api(
        name: str = typer.Option(..., "--name", help="Name of the API"),
        api_version: str = typer.Option("1.0", "--api-version", help="Version of the API"),
        description: str = typer.Option("", "--description", help="Description of the API"),
        path: str = typer.Option("/demo/http-proxy1", "--path", help="API path"),
        target: str = typer.Option("https://api.gravitee.io/echo", "--target", help="Target URL for the proxy endpoint"),
):
    """Create a new API."""
    logging.info(f"Creating API with name: {name}, version: {api_version}")
    api_url, token = validate_config()
    headers = get_headers(token)
    payload = create_api_payload(name, api_version, description, path, target)

    try:
        response = requests.post(f"{api_url}/management/v2/environments/DEFAULT/apis", headers=headers, json=payload)
        logging.info(f"Response: {response.status_code}, {response.text}")

        if response.ok:
            typer.echo("API created successfully!")
            typer.echo(response.json())
        else:
            typer.echo(f"Error: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        typer.echo(f"An error occurred: {str(e)}")
