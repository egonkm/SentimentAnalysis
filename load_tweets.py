# Load tweets from josn files (bz2 compressed) from the site Internet Archive
# File: archiveteam-twitter-stream-2022-12


from glob import glob
import bz2
import os

files = glob("tweets/**/*.bz2", recursive=True)
SAVE_TO = "tweets.csv"
FIELDS = ["lang", "text"]

def get_tweets(text, fields):

    ps_field = 0
    len_text = len(text)

    while ps_field<len_text:

        result = []

        for field in fields:
            ps_field = text.find(field, ps_field)

            if ps_field==-1: # did not find it
                return None
            
            ps_field = text.find(':"', ps_field)+1

            if ps_field==0: return None

            start = ps_field
            end = None

            while not end:
                ps_end = text.find('"', ps_field+1)

                if ps_end==-1: return None

                if text[ps_end-1]== "\\":
                    ps_field = ps_end+1
                    continue
                end = ps_end+1

            result.append(text[start:end])
            ps_field = end+1

        yield result
                


def main(files=files, output=SAVE_TO, fields=FIELDS):

    with open(output, "w") as f:
        f.write(", ".join(fields)+"\n")

    for file in files:
        
        print(file)
        # Open the .bz2 file in binary read mode
        with bz2.BZ2File(file, 'rb') as file:
        # Read the decompressed data
            text = file.read().decode()

            with open(output, "a") as f:
                last_one = []

                for tweet in get_tweets(text, fields):

                    if tweet is None: break
                    if tweet == last_one: continue

                    last_one = tweet
                    # print(tweet)
                    f.write(", ".join(tweet)+"\n")
        
        


if __name__ == "__main__":

    main()

        
