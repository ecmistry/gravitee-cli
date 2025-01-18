import typer
from commands.configure import set_url, set_token, show_config
from commands.list_apis import list_all_apis
from commands.create_api import create_api
from commands.delete_api import delete_api

app = typer.Typer()

# Register commands
app.command(name="configure-url")(set_url)
app.command(name="configure-token")(set_token)
app.command(name="configure-show")(show_config)
app.command(name="list-apis")(list_all_apis)
app.command(name="create-api")(create_api)
app.command(name="delete-api")(delete_api)

if __name__ == "__main__":
    app()
