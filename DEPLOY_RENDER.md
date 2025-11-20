# Deploying Philosophy Notes Bot to Render.com

This guide will help you deploy the Philosophy Notes Bot to Render.com for free 24/7 hosting.

## Prerequisites

Before you begin, make sure you have:

1. **Telegram Bot Token**
   - Go to Telegram and message [@BotFather](https://t.me/BotFather)
   - Send `/newbot` and follow the instructions
   - Save the bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Anthropic API Key** (for AI summaries)
   - Go to [Anthropic Console](https://console.anthropic.com/)
   - Sign up/login and create an API key
   - Save the API key (starts with `sk-ant-api03-...`)

3. **GitHub Account** (to connect to Render)
   - Your code should be in a GitHub repository
   - Render will deploy directly from GitHub

## Deployment Steps

### Step 1: Prepare Your Repository

Make sure these files exist in your repository:
- ✅ `app.py` - Main entry point
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `Python Modules/` - All bot code

### Step 2: Create Render Account

1. Go to [Render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 3: Create New Web Service

1. Click **"New +"** button in Render dashboard
2. Select **"Web Service"**
3. Connect your GitHub repository
4. Choose your `Philosophy-Notes` repository

### Step 4: Configure Service

Render should auto-detect the `render.yaml` configuration. If not, set these manually:

- **Name**: `philosophy-notes-bot` (or any name you prefer)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Plan**: `Free` (starts automatically)

### Step 5: Add Environment Variables

In the Render dashboard, go to **Environment** section and add:

| Key | Value | Notes |
|-----|-------|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather | Required |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Required |

**Important**:
- Click **"Save Changes"** after adding each variable
- Don't include quotes around the values

### Step 6: Deploy!

1. Click **"Create Web Service"**
2. Render will start building and deploying
3. Wait 2-5 minutes for the build to complete
4. You'll see logs in real-time

### Step 7: Verify Deployment

Once deployed, you should see:

```
✓ Build successful
✓ Service live at: https://philosophy-notes-bot.onrender.com
```

To verify it's working:

1. **Check the web endpoint**:
   - Visit: `https://your-service-name.onrender.com/health`
   - Should return: `{"status": "ok", "service": "philosophy-bot"}`

2. **Test your Telegram bot**:
   - Open Telegram
   - Search for your bot by username
   - Send `/start`
   - Bot should respond with welcome message

## Troubleshooting

### Issue: "Application failed to respond" or 404 Error

**Solution**: This was the original problem! The new `app.py` fixes this by:
- Adding root route `/` for Render health checks
- Binding to the PORT environment variable
- Running both bot and API together

If you still see this:
1. Check logs in Render dashboard
2. Verify environment variables are set
3. Make sure you're using the new `app.py` file

### Issue: Bot doesn't respond on Telegram

**Possible causes**:

1. **Bot token not set**:
   - Check Environment Variables in Render
   - Make sure `TELEGRAM_BOT_TOKEN` is correct
   - No quotes, no spaces

2. **Bot already running elsewhere**:
   - Stop any local instances
   - Stop any other cloud instances
   - Only one bot instance can run per token

3. **Check logs**:
   ```
   Render Dashboard → Logs tab
   Look for: "Starting Telegram Bot in background thread..."
   Should see: "✓ Telegram bot thread started"
   ```

### Issue: Build fails

**Common causes**:

1. **Python version**:
   - Render defaults to Python 3.7
   - Add environment variable: `PYTHON_VERSION=3.11.0`

2. **Missing dependencies**:
   - Check that `requirements.txt` exists in root
   - Should include: `python-telegram-bot`, `flask`, `anthropic`

3. **Import errors**:
   - Make sure `Python Modules/` directory exists
   - All required files should be in the repo

### Issue: AI summaries not working

**Solution**:
- Check that `ANTHROPIC_API_KEY` is set correctly
- Verify your Anthropic account has credits
- Check logs for API errors

## Render Free Tier Limitations

The free tier has some limitations:

1. **Service sleeps after 15 minutes of inactivity**
   - First request may take 30-60 seconds to wake up
   - Telegram bot will stay active, so messages work immediately
   - Only affects the API endpoints

2. **750 hours/month free**
   - About 31 days of continuous running
   - Should be enough for one service

3. **No persistent disk**
   - Database and vault files stored in memory
   - Will reset when service restarts
   - For production, upgrade to paid plan for persistent storage

## Production Considerations

For serious use, consider:

1. **Upgrade to paid plan** ($7/month):
   - Persistent disk storage
   - No sleep
   - Better performance

2. **Add persistent storage**:
   - Use Render PostgreSQL for database
   - Use S3 or similar for vault files

3. **Monitoring**:
   - Enable Render alerts
   - Monitor bot health
   - Track API usage

## URLs and Endpoints

Once deployed, your service will have:

- **Base URL**: `https://your-service-name.onrender.com`
- **Health check**: `/health`
- **API health**: `/api/health`
- **Sync status**: `/api/sync/<token>/status`
- **Sync file**: `/api/sync/<token>/file?path=<path>`
- **Vault ZIP**: `/api/sync/<token>/vault.zip`

## Updating Your Bot

To update after deployment:

1. Make changes to your code
2. Commit and push to GitHub
3. Render automatically detects changes
4. Auto-deploys the new version
5. Takes 2-5 minutes

Or manually trigger deploy:
- Go to Render dashboard
- Click "Manual Deploy" → "Deploy latest commit"

## Getting Help

If you encounter issues:

1. **Check Render logs**:
   - Dashboard → Your service → Logs tab
   - Look for error messages

2. **Check bot logs**:
   - Should show: "Starting Telegram Bot..."
   - Should show: "Telegram bot thread started"

3. **Test endpoints**:
   ```bash
   curl https://your-service.onrender.com/health
   curl https://your-service.onrender.com/api/health
   ```

4. **Common fixes**:
   - Restart service in Render dashboard
   - Re-deploy from GitHub
   - Check environment variables
   - Verify bot token with BotFather

## Success Checklist

✅ Repository on GitHub
✅ `app.py` exists in root
✅ `requirements.txt` exists in root
✅ `render.yaml` configured
✅ Render account created
✅ Web service created
✅ Environment variables set (TELEGRAM_BOT_TOKEN, ANTHROPIC_API_KEY)
✅ Service deployed successfully
✅ Health check returns 200 OK
✅ Bot responds on Telegram

## Next Steps

Once deployed:

1. Start using your bot on Telegram
2. Send messages to capture thoughts
3. Try `/today` to see your notes
4. Set up Obsidian sync with `/sync` command
5. Wait for daily AI summary at night

Enjoy your 24/7 philosophy assistant! 🧠✨
