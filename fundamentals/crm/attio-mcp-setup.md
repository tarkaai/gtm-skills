---
name: attio-mcp-setup
description: Install and configure the Attio MCP server for Claude Code integration
tool: Attio
difficulty: Setup
---

# Set Up Attio MCP Server

## Prerequisites
- Attio workspace with API access enabled
- Claude Code installed
- Node.js 18+ installed

## Steps

1. **Get your API key.** In the Attio dashboard, access Settings > Developers > API Keys. Create a new key with full read/write access. Copy the key -- you will not see it again. This is a one-time manual setup step required before the MCP can be used programmatically.

2. **Install the MCP server.** Add the Attio MCP server to your Claude Code configuration. In your `.claude/settings.json` or MCP config, add:

```json
{
  "attio": {
    "command": "npx",
    "args": ["-y", "@attio/mcp-server"],
    "env": {
      "ATTIO_API_KEY": "your-api-key-here"
    }
  }
}
```

3. **Verify the connection.** Restart Claude Code and test the MCP by asking it to list your Attio objects. You should see People, Companies, and any custom objects you've created.

4. **Test CRUD operations.** Create a test contact, read it back, update a field, then delete it. This confirms full read/write access is working.

5. **Set up your GTM config.** In your `.gtm-config.json`, set `"crm": "attio"` so all play skills resolve to the Attio fundamentals.

6. **Security note.** Never commit your API key to version control. Use environment variables or a `.env` file that's in your `.gitignore`. If the key is ever exposed, rotate it immediately in Attio settings.
