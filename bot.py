import praw
import time
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_activity.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("RedditPortfolioBot")

# Load environment variables for sensitive information
load_dotenv()

class RedditPortfolioBot:
    def __init__(self):
        """Initialize the Reddit bot with API credentials."""
        logger.info("Initializing bot...")
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'PortfolioBot v1.0 by YourUsername'),
            username=os.getenv('REDDIT_USERNAME'),
            password=os.getenv('REDDIT_PASSWORD')
        )
        self.subreddits_to_monitor = os.getenv('SUBREDDITS_TO_MONITOR', 'learnprogramming,cscareerquestions').split(',')
        self.keywords = os.getenv('KEYWORDS', 'python,machine learning,data science,web development').split(',')
        self.processed_items = set()
        logger.info(f"Bot initialized to monitor: {self.subreddits_to_monitor}")
        logger.info(f"Looking for keywords: {self.keywords}")

    def _should_respond(self, text):
        """Determine if the bot should respond based on keywords in the text."""
        text = text.lower()
        return any(keyword.lower() in text for keyword in self.keywords)

    def _create_response(self, submission):
        """Create a personalized response based on submission content."""
        title = submission.title.lower()
        
        # Customize response based on detected keywords
        if 'python' in title:
            return ("I noticed you're discussing Python! I could share some helpful resources "
                    "or discuss your specific Python question if you'd like.")
        elif 'machine learning' in title or 'data science' in title:
            return ("As someone working with ML/data science, I'd be happy to discuss your "
                    "question or share some insights from my experience in this field.")
        elif 'web development' in title:
            return ("I see you're interested in web development. I've worked on several web projects "
                    "and would be happy to share some thoughts or resources.")
        else:
            return ("I found your post interesting! I'm a developer with experience in Python, "
                    "machine learning, and web development. Would love to discuss more if helpful.")

    def monitor_subreddits(self):
        """Monitor specified subreddits for new submissions matching keywords."""
        subreddits = '+'.join(self.subreddits_to_monitor)
        logger.info(f"Starting to monitor r/{subreddits}")
        
        for submission in self.reddit.subreddit(subreddits).stream.submissions():
            # Skip if already processed
            if submission.id in self.processed_items:
                continue
                
            self.processed_items.add(submission.id)
            
            # Check if submission contains relevant keywords
            if self._should_respond(submission.title + ' ' + submission.selftext):
                logger.info(f"Found relevant submission: {submission.title}")
                
                try:
                    # Respond to the submission
                    response = self._create_response(submission)
                    submission.reply(response)
                    logger.info(f"Replied to submission {submission.id}")
                    
                    # Add some delay to avoid rate limiting
                    time.sleep(5)
                except Exception as e:
                    logger.error(f"Error responding to submission {submission.id}: {str(e)}")
    
    def monitor_comments(self):
        """Monitor comments in specified subreddits for relevant keywords."""
        subreddits = '+'.join(self.subreddits_to_monitor)
        logger.info(f"Starting to monitor comments in r/{subreddits}")
        
        for comment in self.reddit.subreddit(subreddits).stream.comments():
            # Skip if already processed
            if comment.id in self.processed_items:
                continue
                
            self.processed_items.add(comment.id)
            
            # Check if comment contains relevant keywords
            if self._should_respond(comment.body):
                logger.info(f"Found relevant comment: {comment.id}")
                
                try:
                    # Respond to the comment
                    response = self._create_response(comment.submission)
                    comment.reply(response)
                    logger.info(f"Replied to comment {comment.id}")
                    
                    # Add some delay to avoid rate limiting
                    time.sleep(10)
                except Exception as e:
                    logger.error(f"Error responding to comment {comment.id}: {str(e)}")

if __name__ == "__main__":
    bot = RedditPortfolioBot()
    
    try:
        # Run the bot to monitor submissions
        bot.monitor_subreddits()
    except KeyboardInterrupt:
        logger.info("Bot shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")