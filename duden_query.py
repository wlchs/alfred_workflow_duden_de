#!/usr/local/bin/python3

from urllib import request, error
from sys import argv
from json import dumps
from urllib.parse import quote
from unicodedata import normalize
from bs4 import BeautifulSoup

query = argv[1]
normalized_query = normalize('NFC', query)
url = "https://www.duden.de/suchen/dudenonline/" + quote(normalized_query)
alfred_response = {
      "items": []
}

article_strings = {
   'maskulin': 'der',
   'feminin': 'die',
   'neutrum': 'das'
}

def getArticles(description):
   articles_found = []

   for article in article_strings.keys():
      if article in description.lower():
         articles_found.append(article_strings[article])

   return articles_found

try:
   response = request.urlopen(url)
   content = response.read().decode('utf-8')

   soup = BeautifulSoup(content, 'html.parser')
   s = soup.findAll('section', class_='vignette')
   for match in s:
      title = match.find('a', class_='vignette__label').find('strong').text
      description = match.find('p', class_='vignette__snippet').text.strip()
      link = match.find('a').get('href')

      articles = getArticles(description)
      if articles:
         title = ' / '.join(articles) + ' ' + title
      
      alfred_response["items"].append({
         "uid": title,
         "title": title,
         "subtitle": description,
         "arg": link
      })

except error.HTTPError as err:
   ...

print(dumps(alfred_response))
