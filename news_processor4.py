import nltk
from textblob import TextBlob
import tkinter as tk
from GoogleNews import GoogleNews as news
import time
import re

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def load_locations_from_file(file_path):
    locations = []
    with open(file_path, 'r') as file:
        for line in file:
            location = line.strip()  # Remove leading/trailing whitespace
            if location:
                locations.append(location)
    return locations

# Specify the path to your locations text file
locations_file_path = 'Kelurahan_jawabarat.txt'  # Update this with the actual path to your text file

# Load locations from the file and add them to your locations_list
locations_list = load_locations_from_file(locations_file_path)

def extract_locations_from_title(title):
    locations = []
    # Convert title to lowercase for case-insensitive matching
    title = title.lower()
    for location in locations_list:
        # Use regular expressions to find locations in the title (case-insensitive)
        if re.search(rf'\b{location}\b', title, re.IGNORECASE):
            locations.append(location)
    return locations

def summarize_realtime_news():
    news_client = news(lang='id', region='ID')
    news_client.search('crime OR protest OR begal OR tawuran OR demo')
    max_requests_per_minute = 5
    wait_time = 60
    request_count = 0

    while request_count < max_requests_per_minute:
        try:
            news_client.get_page(3)
            news_results = news_client.result()
            if news_results:
                for article in news_results:
                    print(f'Title: {article["title"]}')
                    print(f'Link: {article["link"]}')
                    locations = extract_locations_from_title(article["title"])
                    if locations:
                        print(f'Location: {", ".join(locations)}')
                    analysis = TextBlob(article["desc"])
                    print(f'Polarity: {analysis.polarity}')
                    print(f'Sentiment: {analysis.sentiment}')
                    print('-' * 50)
            request_count += 1
        except Exception as e:
            if '429' in str(e):  # Check if the exception message contains '429'
                print('Rate limit exceeded. Waiting for a while...')
                time.sleep(wait_time)
            else:
                print(f'An error occurred: {str(e)}')

    root = tk.Tk()
    root.title('Real-time News Summarizer')
    root.geometry('1200x600')
    root.mainloop()

summarize_realtime_news()
