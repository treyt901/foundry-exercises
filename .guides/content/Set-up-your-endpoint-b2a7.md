# Set up your endpoint

First things first: the Prompt Lab you'll use in Part 2 talks to **your**
Azure OpenAI deployment, so it needs your endpoint details in a file called
**`.env`** — exactly like the chat lab. We'll do this together now so that
everything just works later.

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
> the Deployments page. Remember it — in Part 1 you'll explore the catalog
> where the model behind your deployment lives.

**Save the file** (`Ctrl/Cmd + S`) when you're done, then continue to Part 1.
