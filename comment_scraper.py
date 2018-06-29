from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from praw.models import MoreComments

import re


class Subreddit:

    def __init__(self, name, num_submissions, submission_list, num_comments, comment_list, num_comments_read):
        self.name = name
        self.num_submissions = num_submissions
        self.submission_list = submission_list
        self.num_comments = num_comments
        self.comment_list = comment_list
        self.num_comments_read = num_comments_read

def scrape(reddit_bot, subreddit_names, num_submissions, num_comments, tree_depth):

    #Set stop words to english
    stop_words = set(stopwords.words('english'))

    submission_list = []

    filtered_comment = []
    filtered_comment_list = []

    subreddit_list = []

    read = 0
    counter = 0

    for subreddit_name in subreddit_names:

        #Get subreddit object
        subreddit = get_subreddit(reddit_bot, subreddit_name)

        print("Gathering %d comments from top %d submissions in %s..." % (num_comments, num_submissions, subreddit_name))

        #Gather top level comments from x number of submissions inside of subreddit
        for submission in subreddit.top(limit = num_submissions):
            #print("Submission title: %s (contains %d comments) \n" % (submission.title, len(submission.comments)))

            #Add submission title to list of submissions
            submission_list.append(submission.title)

            for comment in submission.comments[:num_comments]:

                counter += 1

                if isinstance(comment, MoreComments):
                    continue

                else:
                    #Clean the comment and tokenize
                    comment_tokens = word_tokenize(str(clean(comment.body)))

                #Skip empty comments
                if(len(comment_tokens) == 0):
                    continue

                else:
                    read += 1
                    #Remove stopwords from tokenized comment
                    for word in comment_tokens:
                        if word not in stop_words:
                            filtered_comment.append(word)

                    filtered_comment_list.append(' '.join(filtered_comment))

                    #print("Filtered comment: %s \n" % str(' '.join(filtered_comment)))

                    filtered_comment = []

        print("Successfully parsed %d comments out of %d --- %.2f percent \n" % (read, counter, 100*(read/counter)))

        counter = 0
        read = 0

        #Construct list of subreddit objects
        subreddit_list.append(Subreddit(subreddit_name, num_submissions, submission_list, num_comments, filtered_comment_list, len(filtered_comment_list)))

        filtered_comment_list = []

    return subreddit_list

def clean(comment):

    #Remove parentheses
    re_p = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", comment)

    #Remove links
    re_l = re.sub(r"http\S+|([\(\[]).*?([\)\]])", "", re_p)

    #Remove special characters
    re_s = re.sub(r"[^A-Za-z \—]+", " ", re_l)

    #Remove excess white space
    filtered_comment = " ".join(re_s.split())

    return filtered_comment


def get_subreddit(reddit_bot, subreddit_name):
    subreddit_obj = reddit_bot.subreddit(subreddit_name)
    return subreddit_obj

def get_tags(subreddit_objects):

    subreddit_tag_list = []
    numeric_tag_list = []

    print("Gathering comment tags... \n")

    for i in range(len(subreddit_objects)):
        length = len(subreddit_objects[i].comment_list)
        while length > 0:
            subreddit_tag_list.append(subreddit_objects[i].name)
            numeric_tag_list.append(i)
            length -= 1

    print("Successfully tagged: %d comments \n" % len(subreddit_tag_list))

    return subreddit_tag_list, numeric_tag_list


def bundle_comments(subreddit_objects):

    bundled_comment_list = []
    
    print("Bundling up comments from all subreddits... \n")

    for i in range(len(subreddit_objects)):
        for comment in subreddit_objects[i].comment_list:
            bundled_comment_list.append(comment)

    print("Successfully bundled: %d comments \n" % len(bundled_comment_list))

    return bundled_comment_list



