import config
import praw

import comment_scraper as cs


def main():

    #Bot login
    reddit_bot = login()

    subreddit_names = list(str(input("Enter the names of the subreddits (separated by commas) that you would like to analyze: ")).split(","))

    #Values can be changed to collect more/less data
    num_submissions = 1
    num_comments = 1
    tree_depth = 1

    #Scrape comments from subreddits
    cs.scrape(reddit_bot, subreddit_names, num_submissions, num_comments, tree_depth)

    
def login():

    reddit_bot = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = config.user_agent)

    return reddit_bot


if __name__ == '__main__':
    main()