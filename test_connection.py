"""Quick connection check for the Foundry Exercises Prompt Lab.

Run from the guide's "Test my connection" button (bash lab.sh test) or
directly with:  python3 test_connection.py

Reads the student's .env, makes one tiny chat-completions call, and prints
a friendly diagnosis of anything that's wrong so students can fix their
configuration BEFORE starting the exercises. Exit code 0 = everything works.
"""

import os
import sys

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    AzureOpenAI,
    NotFoundError,
    OpenAIError,
)

load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21").strip()


def fail(*lines):
    for line in lines:
        print(line)
    print("\nFix the value(s) in .env, save, and press the test button again.")
    sys.exit(1)


print("🔌 Testing your Azure OpenAI connection…\n")

# --- 1. Are all the values filled in? ---------------------------------------
missing = [
    name
    for name, value in [
        ("AZURE_OPENAI_ENDPOINT", ENDPOINT),
        ("AZURE_OPENAI_API_KEY", API_KEY),
        ("AZURE_OPENAI_DEPLOYMENT", DEPLOYMENT),
    ]
    if not value
]
if missing:
    fail(
        "❌ Your .env file is missing these values:",
        *[f"   • {name}" for name in missing],
        "",
        "   Open .env in the file tree, paste in the values from the Azure",
        "   portal (Keys and Endpoint + Deployments pages), and save.",
    )

if not ENDPOINT.startswith("https://"):
    fail(
        "❌ AZURE_OPENAI_ENDPOINT doesn't look like a URL.",
        f"   You have:  {ENDPOINT}",
        "   It should look like:  https://my-openai-resource.openai.azure.com/",
    )

print("✅ .env has all the required values")

# --- 2. Can we actually reach the deployment? --------------------------------
print(f"⏳ Calling your deployment '{DEPLOYMENT}'…\n")
try:
    client = AzureOpenAI(
        azure_endpoint=ENDPOINT, api_key=API_KEY, api_version=API_VERSION
    )
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[{"role": "user", "content": "Reply with exactly: Connection successful"}],
        max_tokens=10,
    )
    reply = (response.choices[0].message.content or "").strip()
except AuthenticationError:
    fail(
        "❌ Azure rejected your API key (401 Unauthorized).",
        "   Copy KEY 1 from your resource's 'Keys and Endpoint' page again —",
        "   watch for missing characters or extra spaces.",
    )
except NotFoundError as exc:
    fail(
        "❌ Azure couldn't find that deployment (404).",
        f"   The error was: {exc}",
        "",
        "   Two usual causes:",
        "   • AZURE_OPENAI_DEPLOYMENT must be the NAME YOU GAVE the deployment",
        "     on the Deployments page — not the model name.",
        "   • AZURE_OPENAI_ENDPOINT should be just the base URL, like",
        "     https://my-openai-resource.openai.azure.com/",
    )
except APIConnectionError:
    fail(
        "❌ Couldn't reach that endpoint at all.",
        f"   You have:  {ENDPOINT}",
        "   Check the URL for typos — it comes from the 'Keys and Endpoint'",
        "   page of your Azure OpenAI resource.",
    )
except APIStatusError as exc:
    fail(
        f"❌ Azure answered with an error (HTTP {exc.status_code}).",
        f"   {exc}",
        "   Read the message above — it usually names the setting to fix.",
    )
except OpenAIError as exc:
    fail("❌ The request failed:", f"   {exc}")

print(f'✅ Success! Your model replied: "{reply}"')
print("\n🎉 Everything works — you're ready to continue with the assignment.")
sys.exit(0)
