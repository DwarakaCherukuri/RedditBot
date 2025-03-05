# Reddit Portfolio Bot

A Python-based Reddit bot that monitors specific subreddits for relevant discussions and automatically responds with helpful information. This project demonstrates proficiency in:

- Python programming
- API integration (Reddit API via PRAW)
- Environment configuration management
- Logging and error handling
- Real-time data processing

## Features

- Monitors multiple subreddits for new posts and comments
- Identifies relevant content using customizable keywords
- Generates contextual responses based on post content
- Implements proper rate limiting to respect Reddit's API rules
- Provides detailed logging for monitoring and debugging

## Setup Instructions

### Prerequisites
- Python 3.6+
- Reddit account
- Reddit API credentials (client ID and secret)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/reddit-portfolio-bot.git
cd reddit-portfolio-bot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Reddit credentials:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=PortfolioBot v1.0 by YourUsername
SUBREDDITS_TO_MONITOR=learnprogramming,cscareerquestions
KEYWORDS=python,machine learning,data science,web development
```

### Getting Reddit API Credentials

1. Visit [Reddit's App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the required information:
   - Name: RedditPortfolioBot
   - App type: Script
   - Description: A bot that responds to programming questions
   - About URL: (Your GitHub profile or project URL)
   - Redirect URI: http://localhost:8080
4. Click "Create app"
5. Note your client ID (the string under your app name) and client secret

## Usage

Run the bot with:
```bash
python bot.py
```

The bot will start monitoring the specified subreddits for new submissions and comments containing your keywords.

## Customization

- Edit the `.env` file to change which subreddits to monitor
- Modify the keywords list to target specific topics
- Customize response templates in the `_create_response` method

## Technical Implementation

The bot uses a streaming approach to monitor Reddit in real-time, processing new submissions and comments as they are posted. It implements:

- Environment-based configuration for security
- Comprehensive logging for debugging and monitoring
- Error handling to ensure stability
- Rate limiting to comply with API requirements

## Future Improvements

Potential enhancements for this project:
- Sentiment analysis to better understand post context
- Machine learning for response generation
- Database integration to track interactions
- Advanced analytics on gathered data
- Web dashboard for monitoring and configuration

## License

MIT License

## Contact

For questions or feedback about this project, please reach out to me at [your email] or connect on [LinkedIn/GitHub/etc].