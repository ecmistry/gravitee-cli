import typer
import json
import re
from config import load_config, save_config

def set_url(api_url: str = typer.Option(..., "--api-url", help="Set the Gravitee APIM API URL")):
    """Set the Gravitee APIM API URL."""
    validate_url(api_url)
    config = load_config()
    config["api_url"] = api_url
    save_config(config)
    typer.echo(f"Gravitee APIM API URL set to: {api_url}")

def set_token(token: str = typer.Option(..., "--token", help="Set the API Bearer Token")):
    """Set the API Bearer Token."""
    config = load_config()
    config["bearer_token"] = token
    save_config(config)
    typer.echo("Bearer Token configured successfully!")

def show_config():
    """Show current configuration."""
    config = load_config()
    if not config:
        typer.echo("No configuration found.")
    else:
        typer.echo("Current Configuration:")
        typer.echo(json.dumps(config, indent=4))

def validate_url(url: str):
    """Validate the provided API URL."""
    regex = re.compile(
        r'^(https?://)'          # Match http:// or https://
        r'([a-zA-Z0-9-]+\.)+'    # Allow alphanumeric and hyphenated domain parts
        r'[a-zA-Z]{2,}$'         # Match valid top-level domains
    )
    if not regex.match(url):
        raise ValueError(f"Invalid URL: {url}")
