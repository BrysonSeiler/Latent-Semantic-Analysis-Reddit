import praw

import config
import k_means as km
import semantic_analysis as sa
import submission_scraper as ss


def main():

    #Bot login
    reddit_bot = login()

    #Get user input for which subreddits to analyze
    subreddit_names = list(str(input("Enter the names of the subreddits (separated by commas) that you would like to analyze: ")).split(","))

    #Values can be changed to collect more/less data (Praw has a limit of 1000)
    num_submissions = 1000

    #Scrape submission titles from chosen subreddits
    subreddit_objects = ss.scrape(reddit_bot, subreddit_names, num_submissions)

    #Bundle together all submission titles from all subreddits
    submissions = ss.bundle_submissions(subreddit_objects)

    #Tag each submission based off of which subreddit it came from
    subreddit_tags, numeric_tags = ss.get_tags(subreddit_objects)

    #Learn vocabulary
    data = sa.run_lsa(len(submissions), submissions, subreddit_tags, numeric_tags, subreddit_names)

    #Cluster data with k-means
    km.run_kmeans(len(subreddit_names), data.lsa_matrix, numeric_tags)


def login():

    print("Logging in... \n")

    reddit_bot = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = config.user_agent)

    return reddit_bot


if __name__ == '__main__':
    main()
