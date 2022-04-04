from datetime import datetime, time, date
import re
import json

import sqlalchemy as db
from sqlalchemy import func, text
from sqlalchemy.sql.expression import column, table

class generate:

    def __init__(self, i, o):
        self.input = i
        self.output = o
        self.generate()

    def generate(self):
        start_time = datetime.now()
        file_data = open(self.input, 'r', encoding="UTF8").read()
        history = json.loads(file_data, encoding="UTF8")
 
        engine = db.create_engine('sqlite:///' + self.output)
        connection = engine.connect()
        metadata = db.MetaData()
        metadata.bind = engine

        videos_history = db.Table('videos', metadata,
              db.Column('Id', db.Integer, primary_key=True, autoincrement=True),
              db.Column('timestamp', db.DateTime),
              db.Column('title', db.String(255)),
              db.Column('url', db.String(255)),
              db.Column('channel', db.String(255)),
              db.Column('channel_url', db.String(255)),
              # db.Column('is_shorts', db.Boolean),
              db.Column('is_music', db.Boolean),
              )
        
        metadata.create_all(engine)
        conn = engine.connect()

        x = len(history)
        totalcount = len(history)
        count = 1
        
        for videos in history:
            service = videos['header']
            title = videos['title']
            title_new = title.lstrip('Watched').lstrip()
            #time_reformat = re.sub(r'[Z]','', videos['time'])
            #videos_newtime = datetime.timestamp(datetime.fromisoformat(time_reformat).strftime("%Y-%m-%d %H:%M:%S"))
            
            # time parsing
            try:
                videos_newtime = datetime.strptime(videos['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                videos_newtime = datetime.strptime(videos['time'], "%Y-%m-%dT%H:%M:%SZ")
            #print(videos_newtime)

            if service == "YouTube Music":
                is_music = True
            else:
                is_music = False

            if videos['title'] == "Visited YouTube Music":
                print (f"Processed: {count}/{totalcount} : Visited YouTube Music data skipped.")
                x -= 1
            elif videos['title'] == "a video that has been removed":
                print (f"Processed: {count}/{totalcount} : Removed video has been skipped.\r")
                x -= 1
            elif re.match("\Astory from", videos['title']):
                print (f"Processed: {count}/{totalcount} : YouTube stories data skipped.\r")
                x -= 1
            elif "titleUrl" not in videos:
                print (f"Processed: {count}/{totalcount} : Empty link has been skipped.\r")
                x -= 1
            elif "subtitles" not in videos:
                x -= 1
                add_record = videos_history.insert().values(
                        title=title_new, url=videos['titleUrl'], channel='Unknown channel', channel_url='null', timestamp=videos_newtime)
                result = connection.execute(add_record)
                
                print (f"Processed: {count}/{totalcount} : {title_new}\r", end="")

            else:
                channel_info = videos['subtitles'][0]

                add_record = videos_history.insert().values(
                        title=title_new, url=videos['titleUrl'], channel=channel_info['name'], channel_url=channel_info['url'], timestamp=videos_newtime, is_music=is_music)
                result = connection.execute(add_record)
                x = x - 1
                print (f"Processed: {count}/{totalcount} : {title_new}\r", end="")
            count += 1
        
        conn.close()
        end_time = datetime.now()
        elapsed = end_time-start_time
        print(elapsed)
