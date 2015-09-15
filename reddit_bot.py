import praw
import time

r = praw.Reddit(user_agent = "Reddit bot for self-learning python by Albert Chung /u/ChickenChopSuey")
r.login
print("Logging in.")

words_to_match = ['chicken chop suey']
cache = []

def run_bot():
    print("Grabbing subreddits.")
    subreddit = r.get_subreddit("test")
    print("Grabbing comments.")
    comments = subreddit.get_comments(limit=20)

    for comment in comments:
        comment_text = comment.body.lower()
        isMatch = any(string in comment_text for string in words_to_match)
        if comment.id not in cache and isMatch:
            print("Match found. Comment ID: " + comment.id)
            comment.reply('Chicken chop suey is delicious.')
            print("Reply successful.")
            cache.append(comment.id)
    print("Loop finished. Sleeping.")

while True:
    run_bot()
    time.sleep(120)

