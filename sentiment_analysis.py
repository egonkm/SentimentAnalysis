# -*- coding: utf-8 -*-
"""Sentiment analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WBG8_JXyyn3lT59IIKGuBojPppV_MPqf
"""

# let's read the tweets we will use for sentiment analysis from a file
# these tweets come from The Internet Archive

import csv

TWEETS_FILE =  "1ktweets_en.csv"

!pip install -qU langchain-mistralai

from langchain_mistralai import ChatMistralAI
# let's use mistral for the sentiment analysis

key = "your key here"

model = ChatMistralAI(model="mistral-small-latest", # mistral-large-latest",
                      api_key=key)

# Positive, negative or neutral
# 5 Sentiments

from langchain_core.messages import HumanMessage, SystemMessage
from time import sleep

tweets = []
MIN_LENGTH = 50

# Open the CSV file
with open(TWEETS_FILE, mode='r') as file:

    csv_reader = csv.reader(file)

    for idx, row in enumerate(csv_reader):

        if len(row[1])<MIN_LENGTH: continue

        messages = [
            SystemMessage(
                content=
                """Using one word, classify the text as positive, negative or neutral.
                Generate a list of three words representing the three most important sentiments in the text.
                Do not include the text in your answer.
                Do not include any explanation.
                The output should contain a maximum of four words.
                """
            ),
            HumanMessage(content=row[1]),]

        try:
            result = model.invoke(messages)
        except Exception as e:
            print(str(e))
            continue

        analysis = (row[1], result.content)
        print(idx, analysis[0], "\n", analysis[1])
        tweets.append(analysis)
        sleep(1) #

with open("sentiment.csv", mode='w') as file:
    # Create a CSV writer object
    csv_writer = csv.writer(file)
    # Write each row to the CSV file
    csv_writer.writerows(tweets)

