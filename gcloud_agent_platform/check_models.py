#!/usr/bin/env python3
"""Check which models an API key can reach on the Gemini Enterprise Agent Platform.

The platform's ListModels method rejects API keys (it needs OAuth), so a key
alone cannot enumerate the catalog. Instead this probes candidate model IDs with
countTokens, which does accept API keys and is not billed.

Follows https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start
"""

import argparse
import concurrent.futures
import sys

API_KEY_PLACEHOLDER = "YOUR_GOOGLE_CLOUD_API_KEY"

CANDIDATE_MODELS = [
    "gemini-1.5-pro-002",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro-tts",
    "gemini-2.5-flash-tts",
    "gemini-live-2.5-flash-native-audio",
    "gemini-3-flash-preview",
    "gemini-3-pro-image",
    "gemini-3.1-pro-preview",
    "gemini-3.1-flash-image",
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-lite-image",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.5-transcribe-preview",
    "gemini-3.5-transcribe-live-preview",
    "gemini-3.5-live-translate-preview",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-omni-1.1-flash-preview",
    "gemini-embedding-2",
]


def load_api_key(api_key_file):
    with open(api_key_file, "r") as f:
        api_key = f.read().strip()

    if not api_key or api_key == API_KEY_PLACEHOLDER:
        raise ValueError(
            f"No valid API key found in '{api_key_file}'. "
            f"Replace the placeholder '{API_KEY_PLACEHOLDER}' with a real API key."
        )
    return api_key


def probe(client, api_error, model):
    try:
        response = client.models.count_tokens(model=model, contents="ping")
    except api_error as e:
        if e.code == 404:
            return model, "missing", "not found"
        if e.code in (401, 403):
            return model, "denied", "key not authorized"
        # Reached the model, but it rejected a plain-text countTokens probe.
        return model, "other", f"HTTP {e.code}"
    return model, "ok", f"countTokens={response.total_tokens}"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--api-key-file",
        required=True,
        help="Path to a file containing the API key.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=CANDIDATE_MODELS,
        help="Model IDs to probe. Defaults to a built-in candidate list.",
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
        client = genai.Client(enterprise=True, api_key=load_api_key(args.api_key_file))
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(
            pool.map(lambda m: probe(client, genai.errors.APIError, m), args.models)
        )

    marks = {"ok": "+", "denied": "-", "missing": " ", "other": "?"}
    for model, status, detail in results:
        print(f"{marks[status]} {model:<38} {detail}")

    reachable = sum(1 for _, status, _ in results if status == "ok")
    print(f"\n{reachable} of {len(results)} probed model(s) reachable with this API key.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
