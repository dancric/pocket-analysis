import requests
from pocket import Pocket, PocketException
import webbrowser
import datetime
import time

#Pocket Authorization

def get_request_token(consumer_key):
	url = 'https://getpocket.com/v3/oauth/request'
	data = {'consumer_key': consumer_key, 'redirect_uri': 'localhost'}
	response = requests.post(url, data=data)
	if response.status_code == 200:
		request_token = response.text[5:]
		webbrowser.open("https://getpocket.com/auth/authorize?request_token={0}&redirect_uri={1}".format(request_token, '127.0.0.1'))
		return request_token

def get_access_token(request_token):
	url = 'https://getpocket.com/v3/oauth/authorize'
	data = {'consumer_key': consumer_key, 'code': request_token}
	response = requests.post(url, data=data)
	if response.status_code == 200:
		return response.text.split('&')[0].split('=')[1]

#Outputs a file with a list of articles and also prints the total word count
def analyze(consumer_key, access_token):
	start_of_year = datetime.datetime(2018,1,1,0,0,0)
	timestamp = int(start_of_year.timestamp())
	p = Pocket(consumer_key = consumer_key, access_token=access_token)
	response = p.retrieve(contentType='article', sort='oldest', state='archive', since=timestamp)

	#Let's just assume it works without error checking :)
	articles = [item[1] for item in response['list'].items()]

	articles.sort(key=lambda article: int(article['word_count']), reverse=True)

	print('Total Word Count: {0}'.format(sum([int(article['word_count']) for article in articles])))

	with open('pocket.html', 'w', encoding='utf-8') as file:
		file.write('<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body><ul>')
		for article in articles:
			file.write('<li><a href="{0}">{1}</a> ({2} words / {3})</li>\n'.format(article['resolved_url'], article['resolved_title'], article['word_count'], time.ctime(int(article['time_added']))))
		file.write('</ul></body></html>')