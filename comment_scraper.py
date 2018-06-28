from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import re


#Subreddit object:
    #subreddit name
    #number of submissions gathered
    #submission titles
    #number of comments gathered
    #comments

class Subreddit:

    def __init__(self, name, num_submissions, submission_list, num_comments, comment_list):
        self.name = name
        self.num_submissions = num_submissions
        self.submission_list = submission_list
        self.num_comments = num_comments
        self.comment_list = comment_list


def scrape(reddit_bot, subreddit_names, num_submissions, num_comments, tree_depth):

    #Set stop words to english
    stop_words = set(stopwords.words('english'))

    for subreddit_name in subreddit_names:

        #Get subreddit object
        subreddit = get_subreddit(reddit_bot, subreddit_name)

        print("Gathering %d comments from %d submissions in %s..." % (num_comments, num_submissions, subreddit_name))

        for submission in subreddit.top(limit = num_submissions):
            print(submission.title)










def get_subreddit(reddit_bot, subreddit_name):
    subreddit_obj = reddit_bot.subreddit(subreddit_name)
    return subreddit_obj