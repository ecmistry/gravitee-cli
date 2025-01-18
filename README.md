Here is the updated `README.md` to reflect the usage of the `list-apis` and `create-api` commands:

---

# Gravitee CLI

Gravitee CLI is a command-line interface tool for managing APIs using the Gravitee API Management (APIM) platform. It simplifies API creation, configuration, and management by providing intuitive commands.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
    - [Commands](#commands)
        - [Configure API URL](#configure-api-url)
        - [Configure Bearer Token](#configure-bearer-token)
        - [View Configuration](#view-configuration)
        - [List APIs](#list-apis)
        - [Create API](#create-api)
- [Example Configuration File](#example-configuration-file)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Configure the Gravitee APIM API URL and Bearer Token.
- Create and manage APIs programmatically.
- List all available APIs with pagination support.

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

3. Make the script executable:
   ```bash
   chmod +x gravitee_cli.py
   ```

---

## Configuration

The Gravitee CLI uses a `config.json` file to store the Gravitee APIM API URL and Bearer Token. This file is created automatically when running the configuration commands.

To manually set these values, run:

- Configure the API URL:
  ```bash
  python gravitee_cli.py configure-url "https://api.gravitee.io"
  ```

- Configure the Bearer Token:
  ```bash
  python gravitee_cli.py configure-token "your_api_bearer_token"
  ```

---

## Usage

Run the CLI to see available commands:
```bash
python gravitee_cli.py --help
```

### Commands

#### Configure API URL
Set the Gravitee APIM API URL:
```bash
python gravitee_cli.py configure-url <api_url>
```
Example:
```bash
python gravitee_cli.py configure-url "https://api.gravitee.io"
```

#### Configure Bearer Token
Set the API Bearer Token:
```bash
python gravitee_cli.py configure-token <token>
```
Example:
```bash
python gravitee_cli.py configure-token "your_api_bearer_token"
```

#### View Configuration
Display the current API URL and Bearer Token:
```bash
python gravitee_cli.py show-config
```

#### List APIs
List all available APIs:
```bash
python gravitee_cli.py list-apis
```
This command supports pagination, fetching all APIs and displaying their IDs and names.

Example output:
```plaintext
ID: 12345, Name: Demo API
ID: 67890, Name: Another API
```

#### Create API
Create a new API with a name, description, path, and target URL:
```bash
python gravitee_cli.py create-api --name <api_name> --description <description> --path <api_path> --target <target_url>
```
Example:
```bash
python gravitee_cli.py create-api \
    --name "Event Consumption - HTTP - GET" \
    --description "Event Consumption - HTTP - Proxy" \
    --path "/demo/http-proxy1" \
    --target "https://api.gravitee.io/echo"
```

This will create an API with the specified parameters, including an HTTP listener and a proxy endpoint.

---

## Example Configuration File

After running the configuration commands, a `config.json` file will be created:

```json
{
    "api_url": "https://api.gravitee.io",
    "bearer_token": "your_api_bearer_token"
}
```

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

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

This updated README now clearly explains how to use `list-apis` and `create-api` commands. Let me know if you need further adjustments!