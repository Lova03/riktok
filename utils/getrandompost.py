import requests
import sqlite3
import re
import random

def remove_markdown_links(text):
    markdown_link_regex = re.compile(r'\[([^\]]+)\]\([^)]+\)')
    return markdown_link_regex.sub(r'\1', text)

def shorten_text(text, max_length=1000):
    return text if len(text) <= max_length else text[:max_length] + '...'

def convert_to_sentences_array(text, max_sentences=35):
    sentence_regex = re.compile(r'[^.!?]+[.!?]+')
    sentences = sentence_regex.findall(text)
    return sentences[:max_sentences]

def get_random_post(subreddit):
    url = f'https://www.reddit.com/r/{subreddit}/top.json?limit=100&t=week'
    headers = {'User-agent': 'VideoPostFetcher/0.1 by JusticeFighter69420'}

    try:
        response = requests.get(url, headers=headers)
        posts = response.json()['data']['children']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS usedPosts (id TEXT PRIMARY KEY)''')
        
        top_posts = []
        for post in posts:
            data = post['data']
            if data['ups'] < 100:
                continue
            c.execute('SELECT * FROM usedPosts WHERE id = ?', (data['id'],))
            if c.fetchone() is None:
                top_posts.append(data)

        if not top_posts:
            raise ValueError('No new top posts available.')

        post = random.choice(top_posts)
        c.execute('INSERT INTO usedPosts (id) VALUES (?)', (post['id'],))
        conn.commit()
        conn.close()

        if 'selftext' in post:
            post['selftext'] = remove_markdown_links(post['selftext'])
            post['shortenedText'] = shorten_text(post['selftext'])
            post['sentencesArray'] = convert_to_sentences_array(post['selftext'])

        return {
            'title': post['title'],
            'url': post['url'],
            'score': post['score'],
            'num_comments': post['num_comments'],
            'ups': post['ups'],
            'downs': post.get('downs', 0),
            'selftext': post.get('selftext', ''),
            'shortenedText': post.get('shortenedText', ''),
            'sentencesArray': post.get('sentencesArray', [])
        }

    except requests.RequestException as e:
        print(e)
        raise ValueError('Failed to retrieve posts from Reddit')