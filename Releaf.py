import feedparser
import csv
from selenium import webdriver

#setting up web scraper
dr = webdriver.PhantomJS();
#scraping the rss page
dr.get('http://allafrica.com/misc/tools/rss.html');

#array of feeds to scrape
topics = [];

#array of company data from csv file
company_info = [];

#number to make sure loop skips the first row of the csv file
row_index = 0;

#loops through all of the options in the select field on the rss page
#this creates an array of potential topics
for topic in dr.find_elements_by_tag_name('option'):
	#appends each potential topic to the array
	topics.append(topic.get_attribute('value'))

#opens csv file with company data
with open('rev_rest_africa.csv', 'rb') as csvfile:
		#reader for csv file
		spamreader = csv.reader(csvfile, delimiter=',')
		#loop through file and append information to the array
		for row in spamreader:
			company_info.append(row)

#loop through urls
for topic in topics:
	row_index = 0;
	d = feedparser.parse('http://allafrica.com/tools/headlines/rdf/'+topic+'/headlines.rdf')
	for row in company_info:
		#skip first row
		if row_index == 0:
			row_index = 1;
		else:
			name = row[0]
			#check if name appears in any entry
			for entry in d['entries']:
				title = entry['title']
				#check if name appears in the title
				if(name in title):
					#if it appears, add it to the array
					row.append(entry.link)
					print(entry.link)

#write the updated array to a new csv file 
with open("output.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(company_info)

