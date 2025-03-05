import praw
import time
import logging
import os
import random
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
        self.last_active_time = datetime.now()
        self.daily_response_count = 0
        self.max_daily_responses = 20  # Limit responses to seem more human
        logger.info(f"Bot initialized to monitor: {self.subreddits_to_monitor}")
        logger.info(f"Looking for keywords: {self.keywords}")

    def _should_respond(self, text):
        """Determine if the bot should respond based on keywords and human-like behavior."""
        # Reset daily counter if it's a new day
        now = datetime.now()
        if now.date() > self.last_active_time.date():
            self.daily_response_count = 0
        
        # Don't exceed daily limit
        if self.daily_response_count >= self.max_daily_responses:
            return False
            
        # Occasionally skip some relevant posts (seems more human)
        if random.random() < 0.3:  # 30% chance to skip even if relevant
            return False
            
        # Check for keywords
        text = text.lower()
        for keyword in self.keywords:
            if keyword.lower() in text:
                return True
                
        return False

    def _get_greeting(self):
        """Return a random conversational greeting."""
        greetings = [
            "Hey there! ",
            "Hi! ",
            "Hello! ",
            "Good question. ",
            "",  # Sometimes no greeting
            "Interesting topic. ",
            "I've been working with this recently. "
        ]
        return random.choice(greetings)

    def _get_sign_off(self):
        """Return a random conversational sign-off."""
        sign_offs = [
            " Hope that helps!",
            " Let me know if you have any questions.",
            " Feel free to ask if you need more details.",
            " Good luck!",
            "",  # Sometimes no sign-off
            " Would love to hear how your project goes.",
            " I've been in your position before - you've got this!"
        ]
        return random.choice(sign_offs)

    def _extract_context(self, submission):
        """Extract context from the submission to create a more personalized response."""
        context = {}
        text = (submission.title + " " + submission.selftext).lower()
        
        # Try to identify if the user is a beginner
        beginner_terms = ["beginner", "new to", "starting out", "learning", "first time"]
        context["is_beginner"] = any(term in text for term in beginner_terms)
        
        # Try to identify if they're asking about a career
        career_terms = ["job", "career", "interview", "portfolio", "resume", "hire"]
        context["is_career"] = any(term in text for term in career_terms)
        
        # Try to identify if they're asking for project ideas
        project_terms = ["project", "portfolio", "idea", "build", "create"]
        context["is_project"] = any(term in text for term in project_terms)
        
        # Try to identify specific technologies mentioned
        tech_patterns = {
            "frameworks": ["react", "angular", "vue", "django", "flask", "spring", "laravel"],
            "languages": ["javascript", "python", "java", "c++", "ruby", "go", "rust", "typescript"],
            "databases": ["sql", "mongodb", "postgresql", "mysql", "database"]
        }
        
        context["technologies"] = {}
        for category, terms in tech_patterns.items():
            found_terms = [term for term in terms if f" {term} " in f" {text} "]
            if found_terms:
                context["technologies"][category] = found_terms
                
        return context

    def _create_response(self, submission):
        """Create a personalized, human-like response based on submission content."""
        title = submission.title.lower()
        context = self._extract_context(submission)
        greeting = self._get_greeting()
        sign_off = self._get_sign_off()
        
        # Base responses that will be customized
        python_responses = [
            "I noticed you're discussing Python! I've been using it for about 3 years now. What specific area are you focusing on?",
            "Python has been my go-to language for a while now. It's great for {context}. I'd be happy to share some resources that helped me.",
            "I've been working with Python extensively. The community is incredibly supportive - have you checked out r/learnpython? They helped me a ton when I was starting out."
        ]
        
        ml_responses = [
            "Machine learning is such a fascinating field! I've been experimenting with different algorithms for my projects. Are you working on a specific application?",
            "Data science is my passion too. Starting with scikit-learn and pandas was a game-changer for me. What kinds of datasets are you working with?",
            "ML/AI has so many applications these days. I found starting with simple regression models helped me understand the more complex concepts later."
        ]
        
        web_responses = [
            "Web development has so many paths you can take. Frontend? Backend? Full stack? I started with HTML/CSS/JS basics and then expanded from there.",
            "Building websites was how I got started in programming. Are you interested in a particular framework? React has been my favorite to work with.",
            "Web dev is constantly evolving, which makes it exciting! I've found building small projects from scratch really helped cement my understanding."
        ]
        
        general_responses = [
            "I've been in tech for a few years now and love discussing development concepts. What particular aspect of your project are you looking for input on?",
            "Programming has been both my profession and hobby. What are you trying to build? Maybe I can point you in a helpful direction.",
            "The tech world is huge! I've worked on everything from small scripts to larger applications. What's your background with coding so far?"
        ]
        
        # Customize based on keywords and extracted context
        if 'python' in title or any('python' in tech for tech_list in context["technologies"].values() for tech in tech_list):
            base_response = random.choice(python_responses)
            
            # Customize for beginners
            if context["is_beginner"]:
                base_response = base_response.replace("{context}", "beginners") + " When I started learning Python, I found interactive tutorials really helpful."
            # Customize for career questions
            elif context["is_career"]:
                base_response = base_response.replace("{context}", "job interviews and skill building") + " I've used Python in several professional roles."
            # Customize for project questions
            elif context["is_project"]:
                base_response = base_response.replace("{context}", "building portfolio projects") + " I've built several data analysis projects with it."
            else:
                base_response = base_response.replace("{context}", "so many applications")
                
        elif 'machine learning' in title or 'data science' in title or any('data' in title for title in context["technologies"].values()):
            base_response = random.choice(ml_responses)
        elif 'web development' in title or any('web' in tech or tech in ['react', 'angular', 'vue', 'html', 'css'] for tech_list in context["technologies"].values() for tech in tech_list):
            base_response = random.choice(web_responses)
        else:
            base_response = random.choice(general_responses)
            
        # Assemble final response with greeting and sign-off
        return f"{greeting}{base_response}{sign_off}"

    def handle_rate_limit(self, error_message):
        """
        Parse the rate limit error message and sleep for the required time
        """
        logger.info(f"Handling rate limit: {error_message}")
        
        try:
            # Try to extract the time from the error message
            if "take a break for" in error_message.lower():
                # Extract the number of minutes/seconds
                if "minute" in error_message.lower():
                    time_str = error_message.split("for")[1].split("minute")[0].strip()
                    wait_time = int(time_str) * 60  # Convert minutes to seconds
                elif "second" in error_message.lower():
                    time_str = error_message.split("for")[1].split("second")[0].strip()
                    wait_time = int(time_str)
                else:
                    # Default to 5 minutes if we can't parse
                    wait_time = 300
                    
                # Add a buffer of 10 seconds plus random time (more human-like)
                wait_time += 10 + random.randint(30, 180)
                
                logger.info(f"Rate limited. Sleeping for {wait_time} seconds")
                time.sleep(wait_time)
                return
        except Exception as e:
            logger.error(f"Error parsing rate limit message: {str(e)}")
        
        # If we couldn't parse properly, use a default wait time
        default_wait = 180 + random.randint(30, 120)  # 3-5 minutes
        logger.info(f"Using default wait time of {default_wait} seconds")
        time.sleep(default_wait)

    def monitor_subreddits(self):
        """Monitor specified subreddits for new submissions matching keywords."""
        subreddits = '+'.join(self.subreddits_to_monitor)
        logger.info(f"Starting to monitor r/{subreddits}")
        
        for submission in self.reddit.subreddit(subreddits).stream.submissions():
            # Skip if already processed
            if submission.id in self.processed_items:
                continue
                
            self.processed_items.add(submission.id)
            
            # Add some randomness to timing (more human-like)
            time.sleep(random.randint(3, 15))
            
            # Check if submission contains relevant keywords
            if self._should_respond(submission.title + ' ' + submission.selftext):
                logger.info(f"Found relevant submission: {submission.title}")
                
                try:
                    # Respond to the submission
                    response = self._create_response(submission)
                    submission.reply(response)
                    logger.info(f"Replied to submission {submission.id}")
                    
                    # Update activity counters
                    self.last_active_time = datetime.now()
                    self.daily_response_count += 1
                    
                    # Add randomized delay to avoid rate limiting and appear more human
                    time.sleep(random.randint(90, 240))  # 1.5-4 minutes
                except Exception as e:
                    error_message = str(e)
                    logger.error(f"Error responding to submission {submission.id}: {error_message}")
                    
                    # Handle rate limit errors specifically
                    if "RATELIMIT" in error_message:
                        self.handle_rate_limit(error_message)
                    else:
                        # For other errors, just wait a bit
                        time.sleep(10)
    
    def monitor_comments(self):
        """Monitor comments in specified subreddits for relevant keywords."""
        subreddits = '+'.join(self.subreddits_to_monitor)
        logger.info(f"Starting to monitor comments in r/{subreddits}")
        
        for comment in self.reddit.subreddit(subreddits).stream.comments():
            # Skip if already processed
            if comment.id in self.processed_items:
                continue
                
            self.processed_items.add(comment.id)
            
            # Add some randomness to timing (more human-like)
            time.sleep(random.randint(2, 10))
            
            # Check if comment contains relevant keywords
            if self._should_respond(comment.body):
                logger.info(f"Found relevant comment: {comment.id}")
                
                try:
                    # Respond to the comment
                    response = self._create_response(comment.submission)
                    comment.reply(response)
                    logger.info(f"Replied to comment {comment.id}")
                    
                    # Update activity counters
                    self.last_active_time = datetime.now()
                    self.daily_response_count += 1
                    
                    # Add randomized delay to avoid rate limiting and appear more human
                    time.sleep(random.randint(60, 180))  # 1-3 minutes
                except Exception as e:
                    error_message = str(e)
                    logger.error(f"Error responding to comment {comment.id}: {error_message}")
                    
                    # Handle rate limit errors
                    if "RATELIMIT" in error_message:
                        self.handle_rate_limit(error_message)
                    else:
                        time.sleep(10)

if __name__ == "__main__":
    bot = RedditPortfolioBot()
    
    try:
        # Run the bot to monitor submissions
        bot.monitor_subreddits()
    except KeyboardInterrupt:
        logger.info("Bot shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")