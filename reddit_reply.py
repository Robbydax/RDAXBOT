#!/usr/bin/python
import praw
import pdb
import re
import os
from googletrans import Translator
 

def containsNonAscii(str):
	try:
		str.encode(encoding='utf-8').decode('ascii')
	except UnicodeDecodeError:
        	return True
	else:
		return False

def main():
	cid = "replace with client_id" 
	secret = "replace with secret"
	uname = "replace with your username"
	passwd = "replacec with your password"
	uagent = "replace with a user agent"

	reddit = praw.Reddit(client_id=cid,
                 client_secret=secret,
                 password=passwd,
                 user_agent=uagent,
                 username=uname)
	if not os.path.isfile("replied_posts.txt"):
		posts_replied_to = []
	else:
		with open("replied_posts.txt", "r") as f:
			posts_replied_to = list(filter(None, f.read().split("\n")))

	subreddit_name = 'replace with a subreddit'
	subreddit = reddit.subreddit(subreddit_name)

	for submission in subreddit.hot(limit=10):
		if submission.id not in posts_replied_to:
			for comment in submission.comments:
				if(containsNonAscii(comment.body)):
					translator = Translator()
					original, translated = translator.translate(comment.body).origin, translator.translate(comment.body).text
					language, confidence = translator.detect(comment.body).lang, translator.detect(comment.body).confidence
					confidence = confidence*100
					comment.reply("Detected langauge: {} with {}% confidence.\n\nOriginal text: {}\n\n Translated text: {}\n\n Source code: https://github.com/Robbydax/RDAXBOT.".format(language, confidence, original, translated))
					posts_replied_to.append(submission.id)

	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")

if __name__ == '__main__':
	main()
