from datetime import datetime, time, date
import re
import sqlite3
import json

class generate:

    def __init__(self, i, o):
        self.input = i
        self.output = o
        self.generate()

    def generate(self):

        file_data = open(self.input, 'r', encoding="UTF8").read()
        history = json.loads(file_data, encoding="UTF8")
    
        conn = sqlite3.connect(self.output)
        c = conn.cursor()

        c.execute ("CREATE TABLE IF NOT EXISTS videos (id varchar (16), title varchar (128), url varchar (192), channel varchar (64), channel_url varchar(192), datetime varchar (64))")
        
        x = len(history)
        totalcount = len(history)
        count = 1
        
        for videos in history:
            time_reformat = re.sub(r'[Z]','', videos['time'])
            videos_newtime = datetime.fromisoformat(time_reformat).strftime("%Y-%m-%d %H:%M:%S")
            
            if videos['title'] == "Visited YouTube Music":
                print ("Processed: {count}/{totalcount} : Visited YouTube Music data skipped.")
                x -= 1
            elif videos['title'] == "a video that has been removed":
                print ("Processed: {count}/{totalcount} : Removed video has been skipped.\r")
                x -= 1
            elif re.match("\Astory from", videos['title']):
                print ("Processed: {count}/{totalcount} : YouTube stories data skipped.\r")
                x -= 1
            elif "titleUrl" not in videos:
                print ("Processed: {count}/{totalcount} : Empty link has been skipped.\r")
                x -= 1
            elif "subtitles" not in videos:
                c.execute("insert or ignore into videos values (?, ?, ?, ?, ?, ?)",
                    [ x, videos['title'], videos['titleUrl'], 'Unknown channel', 'null', videos_newtime])
                conn.commit()
                x -= 1
                print (f"Processed: {count}/{totalcount} : {videos['title']}\r", end="")
            else:
                channel_info = videos['subtitles'][0]
                c.execute("insert or ignore into videos values (?, ?, ?, ?, ?, ?)",
                    [ x, videos['title'], videos['titleUrl'], channel_info['name'], channel_info['url'], videos_newtime])
                conn.commit()
                x = x - 1
                print (f"Processed: {count}/{totalcount} : {videos['title']}\r", end="")
            count += 1
        
        conn.close()