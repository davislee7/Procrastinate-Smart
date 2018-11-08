# Author: Davis Lee
# Description: Provides functions to create dictionaries of search terms and
#              associated timestamps as well as lookup functionality

import xmltodict
import urllib
from nltk.corpus import stopwords
import collections as ct

transcriptLink = 'http://video.google.com/timedtext?lang=en&'


def inputLinks():
    links = []
    link = ""
    while link is not "\n":

        link = input("Enter a link (Enter to quit): ")
        if link is not "\n":
            links.append(link)
    return links

# creates all links with xml code
# RETURNS a list of links that are the xml code


def parseLinks(links):

    i = 0

    while i < len(links):
        link = links[i]
        index = link.index('v')
        extension = link[index:]
        links[i] = transcriptLink + extension
        i += 1
    return links

# creates a dictionary from the xml file that is not pretty


def xmlToDict(link):
    file = urllib.request.urlopen(link)
    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    return data

# i changed the dictionary to be more pleasant to look at
# returns a dictionary that maps each word or two word phrase to a time


def buildProperDict(xmlDict):
    stop_words = set(stopwords.words('english'))
    timeDict = ct.defaultdict(list)

    for phraseAndTime in xmlDict['transcript']['text']:

        if '#text' in phraseAndTime:
            time = phraseAndTime['@start']
            phraseString = phraseAndTime['#text']
            phraseString = phraseString.replace('&#39;', '\'')
            phraseString = phraseString.replace('\n', ' ')
            phraseString = phraseString.replace(',', ', ')
            phraseString = phraseString.replace('.', '. ')
            phraseAndTime['#text'] = phraseString
            phraseString = phraseString.replace(', ', ' ')
            phraseString = phraseString.replace('. ', ' ')

            phrase = phraseString.split()
            content = [word for word in phrase if not word in stop_words]

            grams = [x + ' ' + y for x, y in zip(content[:-1], content[1:])]
            grams += content
            for word in grams:
                timeDict[word].append(time)
    return timeDict

# searches the word in the dictionary and returns the link and dictionary


def searchAndDisplay(links, xmlDicts, timeDicts, searchInput):
    resultLinks = []
    resultDescriptions = []

    for i in range(0, len(links)):

        if searchInput in timeDicts[i]:
            for k in range(0, len(timeDicts[i][searchInput])):
                time = timeDicts[i][searchInput][k]

                resultLinks.append(links[i] + '&t=' + time)

                for j in range(1, len(xmlDicts[i]['transcript']['text']) - 1):
                    prev = xmlDicts[i]['transcript']['text'][j-1]
                    item = xmlDicts[i]['transcript']['text'][j]
                    next = xmlDicts[i]['transcript']['text'][j+1]

                    itemDescription = ""
                    if item['@start'] == time:
                        itemDescription = prev['#text'] + ' ' + item['#text']
                        itemDescription += ' ' + next['#text']
                        resultDescriptions.append(itemDescription)
    return resultLinks, resultDescriptions
