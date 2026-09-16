#!/usr/bin/env python3
"""List the models available on the Gemini Enterprise Agent Platform.

Follows https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start
"""

import argparse
import os
import sys

API_KEY_PLACEHOLDER = "YOUR_GOOGLE_CLOUD_API_KEY"
DEFAULT_LOCATION = "global"

USAGE_NOTES = """\
Authentication (pick one):

  API key (Vertex AI express mode):
    python list_models.py --api-key-file /path/to/api_key.txt

  Application Default Credentials (recommended by the docs):
    gcloud auth application-default login
    python list_models.py --project MY_PROJECT_ID

Create an API key from the Gemini Enterprise Agent Platform getting started page:
  https://console.cloud.google.com/agent-platform/overview
"""


def load_api_key(api_key_file):
    with open(api_key_file, "r") as f:
        api_key = f.read().strip()

    if not api_key or api_key == API_KEY_PLACEHOLDER:
        raise ValueError(
            f"No valid API key found in '{api_key_file}'. "
            f"Replace the placeholder '{API_KEY_PLACEHOLDER}' with a real API key."
        )
    return api_key


def build_client(genai, api_key_file, project, location):
    if api_key_file:
        # Express mode: the key identifies the project, so no project/location.
        return genai.Client(enterprise=True, api_key=load_api_key(api_key_file))

    project = project or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise ValueError(
            "Application Default Credentials mode needs a project: pass --project "
            "or set GOOGLE_CLOUD_PROJECT."
        )
    return genai.Client(enterprise=True, project=project, location=location)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=USAGE_NOTES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--api-key-file",
        help="Path to a file containing an API key. Omit to use Application Default Credentials.",
    )
    parser.add_argument(
        "--project",
        help="Google Cloud project ID. Defaults to $GOOGLE_CLOUD_PROJECT. Ignored with --api-key-file.",
    )
    parser.add_argument(
        "--location",
        default=os.environ.get("GOOGLE_CLOUD_LOCATION", DEFAULT_LOCATION),
        help=f"Location to send requests to. Defaults to $GOOGLE_CLOUD_LOCATION or '{DEFAULT_LOCATION}'.",
    )
    args = parser.parse_args()

    try:
        from google import genai
    except ImportError:
        print(
            "The Google Gen AI SDK is not installed. Run: pip install --upgrade google-genai",
            file=sys.stderr,
        )
        return 1

    try:
        client = build_client(genai, args.api_key_file, args.project, args.location)
        models = list(client.models.list())
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except genai.errors.APIError as e:
        print(f"API error: {e}", file=sys.stderr)
        if args.api_key_file and e.code in (401, 403):
            print(
                "\nListing models goes through ModelGardenService, which only accepts "
                "OAuth credentials. Authenticate with ADC instead:\n"
                "  gcloud auth application-default login\n"
                "  python list_models.py --project MY_PROJECT_ID",
                file=sys.stderr,
            )
        return 1

    if not models:
        print("No models found.")
        return 0

    for model in models:
        print(f"- {model.name}")
    print(f"\n{len(models)} model(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
