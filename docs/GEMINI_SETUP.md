# Google Gemini API Setup Guide

This guide will walk you through getting your Google Gemini API key and configuring the Philosophy Notes Bot.

## What is Gemini?

Google Gemini is a powerful AI model that will analyze your philosophy notes and provide thoughtful reflections. It's free to use with generous limits.

## Step 1: Get Your Gemini API Key

### Visit Google AI Studio

1. Go to **[Google AI Studio](https://aistudio.google.com/app/apikey)**
2. Sign in with your Google account

### Create an API Key

3. Click the **"Create API Key"** button
4. Select a Google Cloud project (or create a new one)
5. Your API key will be generated - it looks like: `AIzaSy...`
6. **Copy this key** - you'll need it in the next step

### Important Notes

- **Free Tier**: Gemini offers 60 requests per minute for free
- **Privacy**: Your notes are sent to Google's Gemini API for analysis
- **Security**: Never share your API key or commit it to version control

## Step 2: Configure the Bot

### Create Your Environment File

1. Navigate to your project directory:
   ```bash
   cd Philosophy-Notes
   ```

2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file:
   ```bash
   nano .env
   # or use your favorite editor: code .env, vim .env, etc.
   ```

### Add Your API Keys

Update these lines in `.env`:

```bash
# Your Telegram bot token (from @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Your Gemini API key (from Google AI Studio)
GEMINI_API_KEY=AIzaSy_your_actual_key_here

# Gemini model (recommended: gemini-1.5-pro)
GEMINI_MODEL=gemini-1.5-pro
```

### Save and Close

- If using nano: Press `Ctrl+X`, then `Y`, then `Enter`
- If using vim: Press `Esc`, type `:wq`, press `Enter`

## Step 3: Choose Your Gemini Model

The Philosophy Notes Bot supports two Gemini models:

### gemini-1.5-pro (Recommended)
- **Best for**: Deep philosophical analysis
- **Strengths**: Complex reasoning, nuanced understanding
- **Speed**: Slower but more thoughtful
- **Free tier**: 2 requests per minute

```bash
GEMINI_MODEL=gemini-1.5-pro
```

### gemini-1.5-flash
- **Best for**: Quick daily summaries
- **Strengths**: Fast responses
- **Speed**: Very fast
- **Free tier**: 15 requests per minute

```bash
GEMINI_MODEL=gemini-1.5-flash
```

## Step 4: Verify Setup

Run this to test your configuration:

```bash
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('Checking configuration...')
print(f'Telegram Token: {'✓' if os.getenv('TELEGRAM_BOT_TOKEN') else '✗'}')
print(f'Gemini API Key: {'✓' if os.getenv('GEMINI_API_KEY') else '✗'}')
print(f'Gemini Model: {os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')}')
"
```

You should see all checkmarks (✓).

## Troubleshooting

### "Invalid API Key" Error

**Problem**: The bot can't connect to Gemini

**Solutions**:
1. Check that your API key is correct in `.env`
2. Make sure there are no extra spaces or quotes
3. Verify the key is active in [Google AI Studio](https://aistudio.google.com/app/apikey)
4. Try regenerating the API key

### "Quota Exceeded" Error

**Problem**: You've hit the free tier limit

**Solutions**:
1. Wait a minute and try again
2. Switch to `gemini-1.5-flash` for higher limits:
   ```bash
   GEMINI_MODEL=gemini-1.5-flash
   ```
3. Consider upgrading to a paid plan if you need more

### Rate Limiting

Free tier limits:
- **gemini-1.5-pro**: 2 requests per minute, 50 per day
- **gemini-1.5-flash**: 15 requests per minute, 1500 per day

The bot automatically generates one reflection per day, so you should be fine with free tier.

## Privacy & Security

### What Data is Sent to Gemini?

When the bot generates your daily summary, it sends:
- Your notes from that day
- Timestamps and tags
- No personal information beyond the note content

### Security Best Practices

1. **Never commit `.env` file to git** (already in `.gitignore`)
2. **Rotate API keys regularly** (every 3-6 months)
3. **Don't share API keys** in chat, screenshots, etc.
4. **Use separate keys** for development and production

## Advanced Configuration

### Use Claude Instead of Gemini

If you prefer Anthropic's Claude:

1. Get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
2. Add to `.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your_key_here
   CLAUDE_MODEL=claude-sonnet-4-20250514
   AI_PROVIDER=claude
   ```

### Use Both (Switch Between)

You can have both API keys configured and switch between them:

```bash
# In .env
GEMINI_API_KEY=AIzaSy...
ANTHROPIC_API_KEY=sk-ant...

# Use Gemini (default)
AI_PROVIDER=gemini

# Or use Claude
AI_PROVIDER=claude
```

## Costs

### Gemini Pricing

**Free Tier** (more than enough for personal use):
- gemini-1.5-pro: 50 requests/day
- gemini-1.5-flash: 1,500 requests/day

**Pay-as-you-go** (if you exceed free tier):
- gemini-1.5-pro: $0.00125 per 1K characters
- gemini-1.5-flash: $0.000075 per 1K characters

For typical usage (5-10 notes/day), you'll stay within free tier.

## Testing Your Setup

Once configured, test the bot:

1. Start the bot:
   ```bash
   ./scripts/start_bot.sh
   ```

2. In Telegram:
   - Send `/start` to your bot
   - Send `/setup` to complete setup
   - Send a test note: "Testing [[Gemini]] integration #test"
   - Wait for confirmation

3. At your configured summary time (default 11 PM), you'll receive:
   - Daily summary of your notes
   - Gemini's philosophical reflection
   - Obsidian-formatted file

## Next Steps

Now that Gemini is configured:

1. ✅ Start capturing your thoughts daily
2. ✅ Review evening summaries
3. ✅ Use `/stats` to see patterns
4. ✅ Set up Obsidian sync for visualization

Happy philosophizing! 🧠✨
