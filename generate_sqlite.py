from datetime import datetime, time, date
import re
import sqlite3
import json
from tracemalloc import start


class generate:
    def __init__(self, i, o):
        self.input = i
        self.output = o
        self.generate()

    def generate(self):
        start_time = datetime.now()
        file_data = open(self.input, 'r', encoding="UTF8").read()
        history = json.loads(file_data, encoding="UTF8")
    
        conn = sqlite3.connect(self.output)
        c = conn.cursor()

        c.execute ("CREATE TABLE IF NOT EXISTS videos (id varchar (16), title varchar (255), url varchar (255), channel varchar (64), channel_url varchar(192), timestamp TIMESTAMP)")

        x = len(history)
        totalcount = len(history)
        count = 1
        
        for videos in history:
            service = videos['header']
            title = videos['title']
            #title_new = title[7:].lstrip()
            title_new = title.lstrip('Watched').lstrip()
            time_reformat = re.sub(r'[Z]','', videos['time'])
            #videos_newtime = datetime.timestamp(datetime.fromisoformat(time_reformat).strftime("%Y-%m-%d %H:%M:%S"))
            
            # time parsing
            try:
                videos_newtime = datetime.strptime(videos['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                videos_newtime = datetime.strptime(videos['time'], "%Y-%m-%dT%H:%M:%SZ")
            
            if service == "YouTube Music":
                is_music = True
            else:
                is_music = False

            #print(videos_newtime)

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
                print (f"Processed: {count}/{totalcount} : Empty link has been skipped.\r",)
                x -= 1
            elif "subtitles" not in videos:                
                c.execute("insert or ignore into videos values (?, ?, ?, ?, ?, ?)",
                    [ x, title_new, videos['titleUrl'], 'Unknown channel', 'null', videos_newtime])
                conn.commit()
                x -= 1

                print (f"Processed: {count}/{totalcount} : {title_new}\r")

            else:
                channel_info = videos['subtitles'][0]
                c.execute("insert or ignore into videos values (?, ?, ?, ?, ?, ?)",
                    [ x, title_new, videos['titleUrl'], channel_info['name'], channel_info['url'], videos_newtime ])
                conn.commit()
                x = x - 1
                print (f"Processed: {count}/{totalcount} : {title_new}\r")
            count += 1
        
        conn.close()
        end_time = datetime.now()
        elapsed = end_time-start_time
        print(elapsed)
