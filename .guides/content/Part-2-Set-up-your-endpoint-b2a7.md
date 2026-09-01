# Part 2 — Set up your endpoint

The Prompt Lab talks to **your** Azure OpenAI deployment, so it needs your
endpoint details in a file called **`.env`** — exactly like the chat lab.

### 1. Create your `.env` file

{Create my .env file}(cp -n .env.example .env && echo "Created .env — now open it from the file tree and add your values.")

### 2. Open `.env` and fill it in

In the **file tree** on the left, open the new **`.env`** file. The panel
beside this guide shows `.env.example` so you can see what each value looks
like.

Fill in these values from your Azure OpenAI resource (in the Azure AI Foundry /
Azure portal, under **Keys and Endpoint** and **Deployments**):

| Setting | What it is | Example |
| --- | --- | --- |
| `AZURE_OPENAI_ENDPOINT` | Your resource URL | `https://my-openai.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | One of your two keys | `abc123...` |
| `AZURE_OPENAI_DEPLOYMENT` | The **deployment name** you created (not the model name) | `gpt-4o-mini` |
| `AZURE_OPENAI_API_VERSION` | REST API version (already filled in) | `2024-10-21` |

> **Tip:** `AZURE_OPENAI_DEPLOYMENT` is the name **you** gave your deployment on
> the Deployments page. And notice the connection to Part 1 — the model behind
> your deployment is one you could find in the catalog.

**Save the file** (`Ctrl/Cmd + S`) when you're done, then continue.
