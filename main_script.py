import config
import praw




def main():

    reddit_bot = login()


def login():

    reddit_bot = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = config.user_agent)


if __name__ == '__main__':
    main()