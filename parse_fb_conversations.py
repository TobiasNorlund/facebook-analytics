import json
from lxml import html
from collections import namedtuple
from dateutil import parser
from time import mktime
import datetime
import sys

filepath = sys.argv[1]
date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)

def parse(filepath):

    f = open(filepath, encoding="utf-8")
    tree = html.fromstring(f.read())

    threads = tree.xpath('//div[@class="thread"]')

    conversations = {}
    
    for thread in threads:
        names = ",".join(sorted(thread.text.split(", ")))

        last_time = None
    
        for msg in thread.xpath('.//div[@class="message"]'):
        
            if names not in conversations:
                conversations[names] = []

            msg_time = parser.parse(msg.xpath('.//span[@class="meta"]')[0].text)
            if msg_time == last_time: # Time resolution only minutes, if same minute, use same sequence as appeared in the html
                delta += datetime.timedelta(0,1)
            else:
                delta = datetime.timedelta(0,0)

            message = {}
            message["time"] = msg_time - delta
            message["writer"] = msg.xpath('.//span[@class="user"]')[0].text
            message["text"] = msg.xpath("./following-sibling::p[1]")[0].text
        
            conversations[names].append(message)
            last_time = msg_time
        

    for conv in conversations.keys():
        conversations[conv] = sorted(conversations[conv], key=lambda msg: msg["time"])

    return conversations

if __name__ == "__main__":

    print("Parsing conversations...")
    conversations = parse(filepath)
    print("Writing json...")
    f = open("fb_messages.json", "wb")
    f.write(json.dumps(conversations, default=date_handler, indent=1, ensure_ascii=False).encode('utf8'))
    f.close()
    print("Done")
