# AISA - Automated Identification for Speech Abuse

AISA (Automated Identification for Speech Abuse) is a Discord bot designed to detect hate speech and offensive language in Indonesian. The bot uses natural language processing (NLP) techniques to identify and flag inappropriate messages in Discord servers.

## Features

- **Hate Speech and Abusive Detection**: Identifies hate speech and abusive language in Indonesian.
- **Automatic Warnings**: Sends warnings to users who send inappropriate messages.
- **Mute Repeated Offenders**: Automatically mutes users who repeatedly violate the rules.
- **Easy Integration**: Easily integrated with your Discord server.

### Requirements

- Python 3.8+
- Pip
- Access to Discord API

## Tech Stack

- **Programming Language**: Python
- **Libraries**:
  - `discord.py` - For interacting with the Discord API
  - `dotenv` - For managing environment variables
  - `numpy` - For numerical operations
  - `scikit-learn` - For machine learning algorithms
  - `tensorflow` - For deep learning models
  - `Flask` - For building web server

## Docker Installation

To run AISA using Docker, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/fahrulsn/aisa-bot.git
   cd aisa-bot
   ```
2. **Navigate to the Server Directory**:
   ```bash
   cd server
   ```
3. **Build the Docker Image**:
   ```bash
   docker build -t aisa-bot .
   ```
4. **Create a .env File: Create a .env file in the server directory with the following content**:
   ```bash
   DISCORD_TOKEN=your_discord_bot_token
   ```
5. **Run the Docker Container**:
   ```bash
   docker run -d --name aisa-bot --env-file .env aisa-bot
   ```

## Usage

1. Before inviting the bot, create a role named `Muted` in your Discord server. This role will be used to mute users who repeatedly violate the rules.
2. Invite the bot to your Discord server using the invitation link provided in the [Discord Developer Portal](https://discord.com/developers/applications).
3. Once the bot is invited, it will start monitoring messages in the server to detect hate speech and offensive language.

## Demo

You can invite the demo bot to your Discord server using this [link](https://discord.com/api/oauth2/authorize?client_id=1177191526456098896&permissions=2416126006&scope=bot).
