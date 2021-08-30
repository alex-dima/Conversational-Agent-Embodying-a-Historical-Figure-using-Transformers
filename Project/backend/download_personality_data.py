import requests
from bs4 import BeautifulSoup
import argparse
import json
from nltk import sent_tokenize, word_tokenize
import numpy as np

class PersonalityData:
    def __init__(self, URL: str):
        self.paragraphs = None
        self.phrases = None
        self.topics = None
        self.title = None
        self.picture = None
        self.URL = URL 
        self.fail = None

        self.getData()

    def getData(self):
        def eliminate_first_parenthesis(text):
            opened = 0
            closed = 0
            found = False
            for index, char in enumerate(text):
                if found and opened == closed:
                    ending = index
                    return text.replace(text[begining:ending], '')
                    
                if char == '(':
                    if opened == 0:
                        begining = index
                    opened += 1
                    found = True

                if char == ')':
                    closed += 1
            return text
        
        response = requests.get(url=self.URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            self.title = soup.select_one('#firstHeading').text
            self.picture = soup.select_one('#mw-content-text table.infobox tbody .infobox-image img')['src']

            #Remove Problematic Sequances
            for selection in soup.select('sup[id], sup[class]'):
                selection.decompose()

            for selection in soup.select('small'):
                selection.decompose()

            for selection in soup.select('abbr'):
                selection.decompose()
            
            #Select Paragraphs
            paragraphs = [paragraph.text.strip() for paragraph in soup.select('#mw-content-text .mw-parser-output > p:not([class]), #mw-content-text .mw-parser-output > blockquote > p:not([class])')]
            blockquotes =  [paragraph.text.strip() for paragraph in soup.select('#mw-content-text blockquote > p:not([class])')]
            paragraphs_and_headings = [paragraph.text.strip() for paragraph in soup.select('h2,h3,h4,#mw-content-text .mw-parser-output > p:not([class]), #mw-content-text .mw-parser-output > blockquote > p:not([class])')]
            
            #Eliminate first paranthesis
            paragraphs[0] = eliminate_first_parenthesis(paragraphs[0]) 
            paragraphs_and_headings[0] = eliminate_first_parenthesis(paragraphs_and_headings[0]) 

            #Eliminate bad paragraph:
            badParagraphs = ["Citations", "Footnotes", "Informational notes", "Bibliography", "See also", "References", "External links"]
            paragraphs = [paragraph for paragraph in paragraphs if paragraph not in badParagraphs]
            paragraphs_and_headings = [paragraph for paragraph in paragraphs_and_headings if paragraph not in badParagraphs]
            
            """
            #TOPICS
             topic_no = index of topic in topics
            """
            topics = []
            topic = []
            for paragraph in paragraphs_and_headings:
                if paragraph not in paragraphs:
                    if len(topic) > 0:
                        topics.append(topic)
                        topic = []
                else:
                    topic.append(paragraph)

            topics = ['\n'.join(topic) for topic in topics]

            self.topics = topics

            """
            #PARAGRAPHS
            paragraph_no = index of paragraph in paragraphs
            """

            for quote in blockquotes:
                index = paragraphs.index(quote)
                if paragraphs[index - 1][-1] == ':':
                    paragraphs[index - 1] = f'{paragraphs[index - 1]} "{quote}"'
                    paragraphs.pop(index)
            self.paragraphs = paragraphs

            """
            #SENTENCES
            paragraph_no: paragraph_index
            phrase_no_in_paragraph: sentence_index
            phrase_no_in_page: index of tuple in sentences
            """
            sentences = [(sentence, paragraph_index, sentence_index) for paragraph_index, paragraph in enumerate(paragraphs) for sentence_index, sentence in enumerate(sent_tokenize(paragraph))]
            self.phrases = sentences

            self.fail = False

        except Exception as err:
            print("Something Went Wrong")
            print(err.with_traceback())
            self.fail = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract data from wikipedia page given as argument")
    parser.add_argument("URL", help="URL of the Wikipedia Article", type=str, metavar="URL")
    args = parser.parse_args()
    
    if not args.URL.startswith("https://en.wikipedia.org/wiki/"):
        print("The URL given isn't a wikipedia page")
    
    personality = PersonalityData(args.URL)





"""
Code used for testing:
"""
            # for paragraph in paragraphs[:10]:
            #     print(paragraph)
            #     print()
            
            # for sentence in sentences[:10]:
            #     print(sentence)
            #     print()

            # words = [(sentence, len(word_tokenize(sentence))) for sentence in sentences if len(word_tokenize(sentence))]
            # print(f"Minimum: {min(words, key = lambda val: val[1])}")
            # print(f"Maximum: {max(words, key = lambda val: val[1])}")
            
            # words = [len(word_tokenize(sentence)) for sentence in sentences if len(word_tokenize(sentence)) > 1]
            # apparitions = {}
            # for word in words:
            #     if word in apparitions:
            #         apparitions[word] += 1
            #     else:
            #         apparitions[word] = 1
            # for key, value in apparitions.items():
            #     print(key)
            # print("AAAAAAAAAAAAAAAAAAAAAAA")
            # for key, value in apparitions.items():
            #     print(value)
            # print(len(apparitions))
            # print(f"Mean: {np.mean(words)}")