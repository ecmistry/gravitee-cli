# Gravitee CLI

Gravitee CLI is a command-line interface (CLI) tool designed to simplify the management of APIs using the Gravitee API Management (APIM) platform. It enables users to configure API settings, create APIs, list available APIs, and extend its functionality with ease.

---

## Features

- **API Configuration**:
    - Configure the Gravitee APIM API URL and Bearer Token.
- **API Management**:
    - Create APIs programmatically with customizable parameters.
    - List all available APIs with pagination support.
- **Modular Design**:
    - Easily extend the CLI by adding new commands.
- **Secure Configuration**:
    - Supports environment variables for sensitive data.

---

## Prerequisites

- Python 3.8 or higher.
- Internet connection.
- Access to a Gravitee APIM environment.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd gravitee-cli
   ```

2. Install dependencies:
   ```bash
   pip install typer requests
   ```

3. Make the main script executable:
   ```bash
   chmod +x main.py
   ```

4. (Optional) Set environment variables for secure configuration:
   ```bash
   export GRAVITEE_API_URL="<your_api_url>"
   export GRAVITEE_BEARER_TOKEN="<your_bearer_token>"
   ```

---

## Usage

Run the CLI to see available commands:
```bash
python main.py --help
```

### Configuration Commands

#### Set API URL
Set the Gravitee APIM API URL:
```bash
python main.py configure-cli url --api-url <api_url>
```
Example:
```bash
python main.py configure-cli url --api-url "https://api.gravitee.io"
```

#### Set Bearer Token
Set the API Bearer Token:
```bash
python main.py configure-cli token --token <token>
```
Example:
```bash
python main.py configure-cli token --token "your_api_bearer_token"
```

#### View Configuration
Display the current API URL and Bearer Token:
```bash
python main.py configure-cli show
```

#### Reset Configuration
Reset the configuration to default:
```bash
python main.py configure-cli reset
```

---

### API Management Commands

#### List APIs
List all available APIs:
```bash
python main.py list-apis all
```
Example output:
```plaintext
ID: 12345, Name: Demo API
ID: 67890, Name: Another API
```

#### Create API
Create a new API with a name, description, path, and target URL:
```bash
python main.py create-api create --name <api_name> --description <description> --path <api_path> --target <target_url>
```
Example:
```bash
python main.py create-api create \
    --name "Event Consumption - HTTP - GET" \
    --description "Event Consumption - HTTP - Proxy" \
    --path "/demo/http-proxy1" \
    --target "https://api.gravitee.io/echo"
```

---

## Logging

All actions performed by the CLI are logged to help with debugging and auditing. Use the `--verbose` flag (if implemented) for more detailed output.

---

## Extending the CLI

### Adding New Commands
1. **Create a New Command File**:
    - Add a new Python file in the `commands` directory, e.g., `commands/new_command.py`.

   Example:
   ```python
   import typer
   from config import validate_config
   from helpers import get_headers

   app = typer.Typer()

   @app.command()
   def new_command(param: str):
       api_url, token = validate_config()
       headers = get_headers(token)
       response = requests.get(f"{api_url}/new/endpoint", headers=headers)

       if response.ok:
           typer.echo("Command executed successfully!")
       else:
           typer.echo(f"Error: {response.status_code} - {response.text}")
   ```

2. **Register the Command**:
    - Import the new command in `main.py` and register it:
   ```python
   from commands.new_command import app as new_command_app
   app.add_typer(new_command_app, name="new-command")
   ```

3. **Test the Command**:
    - Run the CLI to verify the new command:
   ```bash
   python main.py new-command --help
   ```

---
## Extending the CLI

### Adding New Functions for API Calls

Follow these steps to add a new function to the CLI for making API calls:

1. **Create a New Command File**:
    - Add a new Python file in the `commands` directory, e.g., `commands/<new_command>.py`.

   Example:
   ```python
   import typer
   from config import validate_config
   from helpers import get_headers
   import requests

   app = typer.Typer()

   @app.command()
   def new_command(param: str):
       """Description of the new command."""
       api_url, token = validate_config()
       headers = get_headers(token)
       response = requests.get(f"{api_url}/new/endpoint", headers=headers, params={"key": param})

       if response.ok:
           typer.echo("Command executed successfully!")
           typer.echo(response.json())
       else:
           typer.echo(f"Error: {response.status_code} - {response.text}")
   ```

2. **Register the Command**:
    - Import the new command in `main.py` and register it with the CLI:
   ```python
   from commands.<new_command> import app as new_command_app
   app.add_typer(new_command_app, name="new-command")
   ```

3. **Test the Command**:
    - Run the CLI to verify the new command:
   ```bash
   python main.py new-command --help
   ```

4. **Add Parameters and Error Handling**:
    - Enhance the function by adding parameters with `typer.Option` or `typer.Argument`.
    - Include error handling for network issues or invalid responses.

   Example:
   ```python
   @app.command()
   def enhanced_command(param: str = typer.Option(..., "--param", help="Description of the parameter")):
       """Enhanced command with better parameter handling."""
       try:
           api_url, token = validate_config()
           headers = get_headers(token)
           response = requests.post(f"{api_url}/enhanced/endpoint", headers=headers, json={"param": param})

           if response.ok:
               typer.echo("Command executed successfully!")
               typer.echo(response.json())
           else:
               typer.echo(f"Error: {response.status_code} - {response.text}")
       except Exception as e:
           typer.echo(f"An error occurred: {str(e)}")
   ```

5. **Update the README**:
    - Document the new command in the README file, including usage examples and expected output.

---

### Troubleshooting

- **Error: API URL or Bearer Token not configured**:
  Ensure you have run `configure-cli url` and `configure-cli token` commands before executing other commands.

- **Error: Invalid JSON format**:
  Check the payload syntax when passing JSON strings.

- **Connection Timeout**:
  Verify that the Gravitee APIM instance is reachable and the API URL is correct.

- **Error: Invalid URL Format**:
  Ensure the provided API URL follows a valid format (e.g., `https://domain.tld`).

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.
