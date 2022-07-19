import json
import os
import time
from tweepy import Stream
from decouple import config
from datetime import datetime
import argparse

global out

class MyListener(Stream):
    def on_data(self, raw_data):
        out.write(json.dumps(json.loads(raw_data)) + "\n")
        return super().on_data(raw_data)

if __name__ == '__main__':

    CLI = argparse.ArgumentParser()
    CLI.add_argument('--seconds', type=int)
    CLI.add_argument('--track', type=str, default=[])
    args = CLI.parse_args()

    API_KEY=config('API_KEY')
    API_KEY_SECRET=config('API_KEY_SECRET')
    ACCESS_TOKEN=config('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET=config('ACCESS_TOKEN_SECRET')

    os.makedirs('data', exist_ok=True)
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    out = open(f'data/tweets-{now}.txt', 'w', encoding='UTF-8')
    
    stream = MyListener(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream.filter(track=args.track, threaded=True)
    time.sleep(args.seconds)
    stream.disconnect()
