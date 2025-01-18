import os
import json
import logging

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from the file."""
    logging.info(f"Loading configuration from {CONFIG_FILE}")
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # Return an empty dictionary if the file is invalid
    return {}

def save_config(config):
    """Save configuration to the file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        raise RuntimeError(f"Failed to save configuration: {e}")

def validate_config():
    """Validate that the API URL and Bearer Token are configured."""
    config = load_config()
    api_url = config.get("api_url")
    token = config.get("bearer_token")

    if not api_url or not token:
        raise ValueError("API URL or Bearer Token is not configured. Use 'configure-cli' to set them.")

    return api_url, token

