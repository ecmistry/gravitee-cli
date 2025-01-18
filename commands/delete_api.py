import typer
import requests
from config import validate_config
from helpers import get_headers

def delete_api(
        env_id: str = typer.Option(..., "--env-id", help="Environment ID"),
        api_id: str = typer.Option(..., "--api-id", help="API ID to delete"),
):
    """Delete an API by its ID."""
    api_url, token = validate_config()
    headers = get_headers(token)

    # Construct the URL
    url = f"{api_url}/management/v2/environments/{env_id}/apis/{api_id}"

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            typer.echo("API successfully deleted.")
        else:
            typer.echo(f"Failed to delete API: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        typer.echo(f"An error occurred: {str(e)}")
