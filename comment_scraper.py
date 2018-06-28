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

    for subreddit_name in subreddit_names:

        #Get subreddit object
        subreddit = get_subreddit(reddit_bot, subreddit_name)

        print("Gathering %d comments from top %d submissions in %s..." % (num_comments, num_submissions, subreddit_name))

        #Gather top level comments from x number of submissions inside of subreddit
        for submission in subreddit.top(limit = num_submissions):
            print("Submission title: %s (contains %d comments) \n" % (submission.title, len(submission.comments)))

            #Add submission title to list of submissions
            submission_list.append(submission.title)

            print(len(submission.comments[:num_comments]))
            for comment in submission.comments[:num_comments]:

                #Clean the comment and tokenize
                comment_tokens = word_tokenize(str(clean(comment.body)))

                #Skip empty comments
                if(len(comment_tokens) == 0):
                    print("Skipping over empty comment...")
                    continue

                else:
                    #Remove stopwords from tokenized comment
                    for word in comment_tokens:
                        if word not in stop_words:
                            filtered_comment.append(word)

                    filtered_comment_list.append(' '.join(filtered_comment))

                    #print("Filtered comment: %s \n" % str(' '.join(filtered_comment)))

                    filtered_comment = []

        print("Successfully parsed %d comments" % len(filtered_comment_list))

        #Construct list of subreddit objects
        subreddit_list.append(Subreddit(subreddit_name, num_submissions, submission_list, num_comments, filtered_comment_list, len(filtered_comment_list)))

        filtered_comment_list = []

    return subreddit_list

def get_subreddit(reddit_bot, subreddit_name):
    subreddit_obj = reddit_bot.subreddit(subreddit_name)
    return subreddit_obj

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