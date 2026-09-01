# Set up your endpoint

First things first: the Prompt Lab you'll use in Part 2 talks to **your**
Azure OpenAI deployment, so it needs your endpoint details in the **`.env`**
file — it's already open in the panel beside this guide. We'll fill it in and
prove it works before anything else.

### 1. Fill in your `.env`

Add these values from your Azure OpenAI resource (in the Azure AI Foundry /
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

**Save the file** (`Ctrl/Cmd + S`).

### 2. Test your connection

Click the button below. It sends one tiny message to your deployment and tells
you exactly what to fix if anything is wrong:

{✅ Test my connection}(bash lab.sh test)

- **🎉 Everything works** → you're set. Continue to Part 1.
- **❌ Something failed** → the message names the exact `.env` value to fix.
  Edit, save, and test again. Don't move on until the test passes — everything
  in Part 2 depends on this connection.

> The very first test may take a minute — it also installs the app's
> dependencies.
