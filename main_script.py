import config
import praw

import comment_scraper as cs
import semantic_analysis as sa

def main():

    #Bot login
    reddit_bot = login()

    #Get user input for which subreddits to analyze
    subreddit_names = list(str(input("Enter the names of the subreddits (separated by commas) that you would like to analyze: ")).split(","))

    #Values can be changed to collect more/less data
    num_submissions = 4
    num_comments = 5
    tree_depth = 1

    #Scrape comments from subreddits chosen
    subreddit_objects = cs.scrape(reddit_bot, subreddit_names, num_submissions, num_comments, tree_depth)
    
    #Bundle together all comments from all subreddits
    comments = cs.bundle_comments(subreddit_objects)

    #Tag each comment based off of which subreddit it came from
    subreddit_tags, numeric_tags = cs.get_tags(subreddit_objects)

    #sa.run_lsa(len(comments), comments, tags, numeric)
    


def login():

    reddit_bot = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = config.user_agent)

    return reddit_bot


if __name__ == '__main__':
    main()