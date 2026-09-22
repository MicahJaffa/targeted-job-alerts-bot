# Targeted Job Alerts Bot

A Python bot that searches for job listings, scores them based on relevance, and sends matching jobs to Slack.

## Features

* Searches for job listings using RapidAPI
* Scores jobs based on relevance
* Sends job alerts to Slack
* Runs automatically with GitHub Actions
* Uses environment variables to keep API keys and tokens secure

## How It Works

```text
Search for Jobs
      ↓
Process Listings
      ↓
Score Jobs
      ↓
Send Matches to Slack
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/MicahJaffa/targeted-job-alerts-bot.git
cd targeted-job-alerts-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a `.env` file in the root directory:

```env
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_APP_TOKEN=your_slack_app_token
RAPIDAPI_KEY=your_rapidapi_key
CHANNEL_ID=your_slack_channel_id
```

Do not commit your `.env` file to GitHub.

Add this to `.gitignore`:

```text
.env
```

### 4. Run the bot

```bash
python app.py
```

## Environment Variables

| Variable          | Description      |
| ----------------- | ---------------- |
| `SLACK_BOT_TOKEN` | Slack bot token  |
| `SLACK_APP_TOKEN` | Slack app token  |
| `RAPIDAPI_KEY`    | RapidAPI key     |
| `CHANNEL_ID`      | Slack channel ID |

## GitHub Actions

The bot can run automatically using GitHub Actions.

Add the following as GitHub repository secrets:

```text
SLACK_BOT_TOKEN
SLACK_APP_TOKEN
RAPIDAPI_KEY
CHANNEL_ID
```

## Project Structure

```text
targeted-job-alerts-bot/
├── app.py
├── job_search.py
├── score.py
├── slack_bot.py
├── requirements.txt
└── .github/
    └── workflows/
```

## Tech Stack

* Python
* RapidAPI
* Slack API
* GitHub Actions
