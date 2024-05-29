import Watch_Game_Script
import pandas as pd
import sys

try:
    Games = int(sys.argv[1])
    dev_level = sys.argv[2]
except: 
    Games = 1
    dev_level = "dev"

print(Games)
print(dev_level)

shuffled_df = pd.read_csv("shuffled_df.csv")

if __name__ == "__main__":

    i = 0
    while i < Games:
        try:
            shuffled_df = pd.read_csv("shuffled_df.csv")
            url = shuffled_df['url'][0]
            season = shuffled_df['season'][0]
            shuffled_df = shuffled_df.drop(index = shuffled_df.index[0])
            if dev_level == "prod":
                    shuffled_df.to_csv('shuffled_df.csv', index = False)
                    print('saved new shuffled')
            print(url)
            Watch_Game_Script.Watch_Game(url, verbose = True)
            i += 1
        except Exception as e:
            print(f"could not run for {e}")
            i += 1
            pass
    