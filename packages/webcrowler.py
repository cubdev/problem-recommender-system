"""
	Web crowler using multi-threading
	@author: Md Abdussamad
"""
import sys, time, json
import requests
import threading
from lxml import html

class Crowler:
	"""
	Generic web crawler. Only need to set no. of threads
	(Exept main) to work simultaneously. By default it's 20.

	Public methods-
	@method get_data: return data as per HTML tags provided.
	"""
	def __init__(self, n_threads=20):
		self.lock = threading.Lock()	# Mutex for critical section
		self.n_threads = n_threads	# Number of threads at a time
		self.data = []			# Store result data
		
	def _crawl(self, url, tags):
		try:
			# timeout=(connect, read)
			# Take connect-timeout above multiples of 3
			page = requests.get(url, timeout=(3.01, 27))

			# Check if page is available
			if page.status_code == requests.codes.ok and page.url == url:
				# Create tree of html tags
				tree = html.fromstring(page.content)
				data = dict()	# Store current page data
				for key in list(tags):
					text = tree.xpath(tags[key])
					data[key] = " ".join([ x.strip().encode('ascii', 'ignore') for x in text ])
				
				self.lock.acquire()
				# Critical section start
				self.data.append(data)
				# Critical section end
				self.lock.release()
				
		except requests.exceptions.RequestException as err:
			print "\nERROR:: {}//{}".format(threading.current_thread(), err)
			return

	def get_data(self, urls, tags):
		"""
		Iterate over urls and collect data.

		@param urls: List of url to crawl
		@param tags: <key, value> pairs of HTML tags

		@return: List of dict
		"""
		self.data = [] # Need to reset everytime
		for url in urls:
			# Default 20 Threads(Exept main thread) at a time
			while(threading.active_count() > self.n_threads):
				time.sleep(0.1)
			# Create new thread
			thread = threading.Thread(target=self._crawl, args=(url, tags))
			thread.start()

		# Wait for threads(Exept main thread)
		# to finish their respective work.
		while (threading.active_count() > 1):
			time.sleep(0.1)

		return self.data

def get_cf_problem_urls(n_data=10, section="ABCDEFG"):
	"""
	Generates all the possible links of problems from
	codeforces.com.
	"""
	base_url = 'http://codeforces.com/problemset/problem/%s/%s'
	urls = list()
	for i in range(n_data):
		for j in section:
			url = base_url % (str(i + 1), str(j))
			urls.append(url)
	return urls

def get_cf_submission_urls(user='e_coder', n_page=10):
	"""
	Generates all the possible links of submission page
	of an user on codeforces.com.
	"""
	base_url = 'http://codeforces.com/submissions/%s/page/%s'
	urls = []
	for i in range(n_page):
		url = base_url % (user, str(i + 1))
		urls.append(url)
	return urls

def get_cf_problem_tags():
	tags = {
		'title': "//div[@class='header']/div[@class='title']/text()",
		'statement': "//div[@class='problem-statement']/div[preceding-sibling::div[@class='header']]/p/text()",
		'contest': "//a[contains(@href, '/contest/')]/text()",
		'tags': "//span[@class='tag-box']/text()"
	}
	return tags

def get_cf_submission_tags():
	tags = {
		'pages': "//span[@class='page-index']/a/text()",
		'sub_id': "//span[@submissionverdict='OK']/@submissionid",
		'tid': "//tr[@data-submission-id='%s']/td/text()",
	}
	return tags

def parse_command():
	import optparse
	parser = optparse.OptionParser()

	parser.add_option('-q', '--query', 
		action="store", dest="query",
		help="query string", default="")

	options, args = parser.parse_args()
	return options

if __name__ == '__main__':
	''' Command line interface '''
	options = parse_command()
	if options.query == '':
		print "Usage: pyhton web_crowler.py -q [query]"
		exit(1)

	c = Crowler()
	if options.query == 'MAKE_DATA':
		data = c.get_data(get_cf_problem_urls(),
			get_cf_problem_tags())

		import pandas as pd
		df = pd.DataFrame(data)
		print df.head()

		df.to_csv('dataset.csv', index = False)
