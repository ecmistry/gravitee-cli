import typer
import os
import json
import requests

# Initialize Typer app
app = typer.Typer()

# Default configuration file path
CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from the file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration to the file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

@app.command()
def configure_url(api_url: str = typer.Argument(..., help="Set the Gravitee APIM API URL")):
    """Set the APIM API URL."""
    config = load_config()
    config["api_url"] = api_url
    save_config(config)
    typer.echo(f"Gravitee APIM API URL set to: {api_url}")

@app.command()
def configure_token(token: str = typer.Argument(..., help="Set the API Bearer Token")):
    """Set the API Bearer Token."""
    config = load_config()
    config["bearer_token"] = token
    save_config(config)
    typer.echo("Bearer Token configured successfully!")

@app.command()
def show_config():
    """Show current configuration."""
    config = load_config()
    if not config:
        typer.echo("No configuration found.")
    else:
        typer.echo("Current Configuration:")
        typer.echo(json.dumps(config, indent=4))

@app.command()
def list_apis():
    """List all APIs using the configured URL and Bearer Token, accommodating for paging."""
    config = load_config()
    api_url = config.get("api_url")
    token = config.get("bearer_token")

    if not api_url or not token:
        typer.echo("Error: API URL or Bearer Token not configured.")
        raise typer.Exit()

    next_page_url = f"{api_url}/management/v2/environments/DEFAULT/apis/?page=1&size=10"

    while next_page_url:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(next_page_url, headers=headers)

        # Debug: Log response content
        typer.echo(f"Response Content: {response.text}")

        if response.ok:
            try:
                apis = response.json()

                # Fetch API data
                data = apis.get("data", [])
                for api in data:
                    typer.echo(f"ID: {api['id']}, Name: {api['name']}")

                # Handle pagination links
                links = apis.get("links", {})
                next_page_url = links.get("next", None)
            except (ValueError, KeyError) as e:
                typer.echo("Error: Unable to parse API response.")
                typer.echo(f"Details: {str(e)}")
                raise typer.Exit()
        else:
            typer.echo(f"Error: {response.status_code} - {response.text}")
            break

@app.command()
def create_api(
        name: str = typer.Option(..., help="Name of the API"),
        api_version: str = typer.Option("1.0", help="Version of the API"),
        description: str = typer.Option("", help="Description of the API"),
        path: str = typer.Option("/demo/http-proxy1", help="API path"),
        target: str = typer.Option("https://api.gravitee.io/echo", help="Target URL for the proxy endpoint"),
):
    """Create a new API."""
    config = load_config()
    api_url = config.get("api_url")
    token = config.get("bearer_token")

    if not api_url or not token:
        typer.echo("Error: API URL or Bearer Token not configured.")
        raise typer.Exit()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "name": name,
        "apiVersion": api_version,
        "description": description,
        "definitionVersion": "V4",
        "type": "PROXY",
        "listeners": [
            {
                "type": "HTTP",
                "paths": [
                    {
                        "path": path
                    }
                ],
                "entrypoints": [
                    {
                        "type": "http-proxy"
                    }
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
                            "target": target
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(f"{api_url}/management/v2/environments/DEFAULT/apis", headers=headers, json=payload)

    if response.ok:
        api_response = response.json()
        typer.echo("API created successfully!")
        typer.echo(json.dumps(api_response, indent=4))
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    app()
