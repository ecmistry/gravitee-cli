import requests
import typer
from config import validate_config
from helpers import get_headers

def update_api(
        env_id: str = typer.Option(..., "--env-id", help="Environment ID"),
        api_id: str = typer.Option(..., "--api-id", help="API ID"),
        name: str = typer.Option(..., "--name", help="API Name"),
        api_version: str = typer.Option(..., "--api-version", help="API Version"),
        description: str = typer.Option(None, "--description", help="API Description")
):
    """Update an existing API's information."""
    try:
        # Validate configuration
        api_url, token = validate_config()

        # Prepare the URL and headers
        endpoint = f"{api_url}/management/v2/environments/{env_id}/apis/{api_id}"
        headers = get_headers(token)

        # Prepare the payload
        payload = {
            "name": name,
            "apiVersion": api_version,
            "definitionVersion": "V4",
            "type": "PROXY",
            "description": description or "",
            "listeners": [
                {
                    "type": "HTTP",
                    "paths": [
                        {"path": "/demo/http-proxy"}
                    ],
                    "entrypoints": [
                        {"type": "http-proxy"}
                    ]
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
                            "configuration": {
                                "target": "https://api.gravitee.io/echo"
                            }
                        }
                    ]
                }
            ]
        }

        # Debugging: Log the payload
        typer.echo("Payload being sent:")
        typer.echo(payload)

        # Send the PUT request
        response = requests.put(endpoint, headers=headers, json=payload)

        # Handle response
        if response.ok:
            typer.echo("API updated successfully!")
            typer.echo(response.json())
        else:
            typer.echo(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")

# Register command with typer
if __name__ == "__main__":
    app = typer.Typer()
    app.command()(update_api)
    app()
