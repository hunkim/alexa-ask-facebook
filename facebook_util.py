import unirest
import json
import random

from datetime import datetime, timedelta
from config import group_id, access_token


def put_comment(post_id, comment):
    url = "https://graph.facebook.com/" + post_id + "/comments/"
    r = unirest.post(url,
                     params={'message': comment,
                             'access_token': access_token})
    print("Status code:", r.code)
    print("out", r.body)


def remove_line_breaks(str):
    return str.replace('\n', ' ').replace('\r', '')[:80]


def get_one_post(post):
    if 'message' not in post:
        return None, None

    return post['id'], \
        remove_line_breaks(post['message']) + \
        " by " + post['from']['name']


def get_new_facebook_feed():
    since = datetime.today() - timedelta(days=1)

    url = "https://graph.facebook.com/" +\
        group_id +\
        "/feed?fields=from,message&" +\
        "comments.limit(100){message,created_time,from,attachment,like_count," +\
        "comments.limit(100){message,created_time,from,attachment,like_count}}" +\
        "&limit=10" +\
        "&since=" + str(since) +\
        "&access_token=" + access_token

    r = unirest.get(url)
    print("Status code:", r.code)
    data = r.body

    posts = data['data']
    if len(posts) > 0:
        post = random.choice(posts)
        return get_one_post(post)

    return None, None

if __name__ == "__main__":
    post_id, post_str = get_new_facebook_feed()
    print(post_id, post_str)
    put_comment(post_id, "OK OK")
