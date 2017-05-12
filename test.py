import json
from pprint import pprint
import datetime
import time

import main


def testEvent(eventjson_file):
    with open(eventjson_file) as data_file:
        event = json.load(data_file)

        res = main.lambda_handler(event, {})
        pprint(res)


testEvent('test_cases/get_feed.json')
testEvent('test_cases/put_comment.json')
