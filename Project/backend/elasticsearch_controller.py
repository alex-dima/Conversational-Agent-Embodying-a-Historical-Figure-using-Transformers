from elasticsearch import Elasticsearch, helpers
from download_personality_data import PersonalityData
import string

class ElasticSearchPersonalities:
    def __init__(self):
        self.connected = None
        self.es_client = None

        self.connect_elasticsearch()
        if self.connected:
            self.initialize_indices()
            

    def connect_elasticsearch(self):
        _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        if _es.ping():
            print('Connection to ElasticSearch SUCCEDED')
            self.connected = True
            self.es_client = _es
        else:
            print('Connection to ElasticSearch FAILED')
            self.connected = False

    def initialize_indices(self):
        #Create Phrase Index Non-Existent:
        phrase_mappings = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    },
                    "paragraph_no": {
                        "type": "integer"
                    },
                    "phrase_no_in_paragraph": {
                        "type": "integer"
                    },
                    "phrase_no_in_page": {
                        "type": "integer"
                    }
                }
            }
        }

        response = self.es_client.indices.create(index="personalities_phrases", body=phrase_mappings, ignore=400)
        if 'acknowledged' in response:
            if response['acknowledged'] == True:
                print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])

        # catch API error response
        elif 'error' in response:
            if response['error']['type'] == 'resource_already_exists_exception':
                print("Index 'personalities_phrases' already exists")
            
            else:
                print ("ERROR:", response['error']['root_cause'])
                print ("TYPE:", response['error']['type'])

        #Create Paragraph Index Non-Existent:
        paragraph_mappings = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    },
                    "paragraph_no": {
                        "type": "integer"
                    }
                }
            }
        }

        response = self.es_client.indices.create(index="personalities_paragraphs", body=paragraph_mappings, ignore=400)
        if 'acknowledged' in response:
            if response['acknowledged'] == True:
                print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
        
        # catch API error response
        elif 'error' in response:
            if response['error']['type'] == 'resource_already_exists_exception':
                print("Index 'personalities_paragraphs' already exists")
            
            else:
                print ("ERROR:", response['error']['root_cause'])
                print ("TYPE:", response['error']['type'])
    

        #Create Topics Index Non-Existent:
            topics_mappings = {
                "mappings": {
                    "properties": {
                        "title": {
                            "type": "text"
                        },
                        "text": {
                            "type": "text"
                        },
                        "topic_no": {
                            "type": "integer"
                        }
                    }
                }
            }

            response = self.es_client.indices.create(index="personalities_topics", body=topics_mappings, ignore=400)
            if 'acknowledged' in response:
                if response['acknowledged'] == True:
                    print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
            
            # catch API error response
            elif 'error' in response:
                if response['error']['type'] == 'resource_already_exists_exception':
                    print("Index 'personalities_topics' already exists")
                
                else:
                    print ("ERROR:", response['error']['root_cause'])
                    print ("TYPE:", response['error']['type'])

            #Create Finder Index if Non-Existent:
            finder_mappings = {
                "mappings": {
                    "properties": {
                        "title": {
                            "type": "text"
                        },
                        "picture": {
                            "type": "text"
                        }
                    }
                }
            }

            response = self.es_client.indices.create(index="personalities_finder", body=finder_mappings, ignore=400)
            if 'acknowledged' in response:
                if response['acknowledged'] == True:
                    print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
            
            # catch API error response
            elif 'error' in response:
                if response['error']['type'] == 'resource_already_exists_exception':
                    print("Index 'personalities_finder' already exists")
                
                else:
                    print ("ERROR:", response['error']['root_cause'])
                    print ("TYPE:", response['error']['type'])


    def add_personality_data(self, URL: str):
        def personality_exists(es_client: Elasticsearch, personality: PersonalityData, index: str):
            query = {
                "query": {
                    "match": {
                        "title": f"{personality.title}"
                    }
                }
            }

            result = es_client.search(index=index, body=query)
            return True if result['hits']['total']['value'] != 0 else False


        personality = PersonalityData(URL)
        if personality.fail:
            print("Couldn't Fetch Personality Data")
            return

        #Add phrases    
        if not personality_exists(self.es_client, personality, "personalities_phrases"):
            phrases_bulk_data = (
                {'_index': "personalities_phrases",
                 '_source': {
                    'title': personality.title,
                    'text': text,
                    'paragraph_no': paragraph_no,
                    'phrase_no_in_paragraph': phrase_no_in_paragraph,
                    'phrase_no_in_page': phrase_no_in_page
                    }
                } for phrase_no_in_page, (text, paragraph_no, phrase_no_in_paragraph) in enumerate(personality.phrases))

            response = helpers.bulk(self.es_client, actions=phrases_bulk_data)    
            print(f"Added {response[0]} phrases to index 'personalities_phrases' for {personality.title}")
        
        else:
            print(f"Index personalities_phrases already contains entries for {personality.title}")
        
        #Add paragraphs
        if not personality_exists(self.es_client, personality, "personalities_paragraphs"):
            paragraphs_bulk_data = (
                {'_index': "personalities_paragraphs",
                 '_source': {
                    'title': personality.title,
                    'text': text,
                    'paragraph_no': paragraph_no
                    }
                } for paragraph_no, text in enumerate(personality.paragraphs))

            response = helpers.bulk(self.es_client, actions=paragraphs_bulk_data)    
            print(f"Added {response[0]} paragraphs to index 'personalities_paragraphs' for {personality.title}")

        else:
            print(f"Index personalities_paragraphs already contains entries for {personality.title}")

         #Add topics
        if not personality_exists(self.es_client, personality, "personalities_topics"):
            topics_bulk_data = (
                {'_index': "personalities_topics",
                 '_source': {
                    'title': personality.title,
                    'text': text,
                    'topic_no': topic_no
                    }
                } for topic_no, text in enumerate(personality.topics))

            response = helpers.bulk(self.es_client, actions=topics_bulk_data)    
            print(f"Added {response[0]} topics to index 'personalities_topics' for {personality.title}")

        else:
            print(f"Index personalities_topics already contains entries for {personality.title}")
         
         #Add personality to finder
        if not personality_exists(self.es_client, personality, "personalities_finder"):
            finder_data = {
                    'title': personality.title,
                    'picture': personality.picture
                }

            response = self.es_client.index(index="personalities_finder", body=finder_data)    
            print(f"Added personality to index 'personalities_finder' for {personality.title}")

        else:
            print(f"Index personalities_finder already contains entries for {personality.title}")

    def run_query(self, question: str, personality: str, index: str) -> str:
        """
        Runs a query for one of the indexes, for now those are "phrases", "paragraphs", "topics" and "heuristic".
        Personality is the title of the HTML article in this implementation.
        Question will be processed into the text to be searched
        """
        def is_included(results, candidate):
            for result in results:
                if candidate in result:
                    return True
            return False

        def parse_question(question):
            def white_space_fix(text):
                return ' '.join(text.split())
            def remove_punc(text):
                exclude = set(string.punctuation)
                return ''.join(ch for ch in text if ch not in exclude)
            def remove_wh_pronouns(text):
                wh_pronouns = ['what', 'when', 'where', 'which', 'who', 'whom', 'whose', 'why', 'how']
                adjectives = ['far', 'many', 'much']
                tokens = text.lower().split()
                return [index for index, value in enumerate(tokens) if (value not in wh_pronouns) and \
                    ((value not in adjectives) or (value in adjectives and tokens[index-1] not in wh_pronouns))]
            
            question = remove_punc(white_space_fix(question))
            indices = remove_wh_pronouns(question)
            return ' '.join(word for index, word in enumerate(question.split()) if index in indices)

        text = parse_question(question)

        if index in ["phrases", "paragraphs", "topics"]:
            if index == "phrases": #will miss 6 gold phrases
                size = 58
            elif index == "paragraphs": #will miss 7 gold paragraphs
                size = 10
            else:
                size = 3 #will miss 11 gold topics
            index = f'personalities_{index}'
            

            query = {
                "size": f"{size}",
                "query": {
                    "bool": {
                        "must":[
                            {
                                "match": {"title": personality}
                            }
                        ],
                        "should":[
                            {
                                "match": {"text": text}
                            }	
                        ]
                    }
                }
            }

            results = self.es_client.search(index=index, body=query)
            results = [result["_source"]["text"] for result in results["hits"]["hits"]]
            
        elif index == "heuristic":
            all_indices = ["personalities_topics", "personalities_paragraphs", "personalities_phrases"]
            all_sizes = [1,8,10]
            results = []
            for index, size in zip(all_indices, all_sizes):
                query = {
                    "size": f"{size}",
                    "query": {
                        "bool": {
                            "must":[
                                {
                                    "match": {"title": personality}
                                }
                            ],
                            "should":[
                                {
                                    "match": {"text": text}
                                }	
                            ]
                        }
                    }
                }
                partial_results = self.es_client.search(index=index, body=query)
                partial_results = [result["_source"]["text"] for result in partial_results["hits"]["hits"]]
                for pres in partial_results:
                    if not is_included(results, pres):
                        results.append(pres)
            
        return '\n'.join(results) 

    def get_finder(self):
        query = {
            "query": {
                "match_all": {}
            }
        }
        results = self.es_client.search(index="personalities_finder", body=query)
        return [{'name': result["_source"]["title"], 'picture': result["_source"]["picture"]} for result in results["hits"]["hits"]]

    def remove_personality(self, name):
        query = {
            "query": 
            {
                "match": 
                {
                    "title": f"{name}"
                }
            }
        }

        self.es_client.delete_by_query(index="personalities_topics", body=query)     
        self.es_client.delete_by_query(index="personalities_paragraphs", body=query)     
        self.es_client.delete_by_query(index="personalities_phrases", body=query)     
        self.es_client.delete_by_query(index="personalities_finder", body=query)     

    def get_personality(self, name):
        query = {
            "query": 
            {
                "match": 
                {
                    "title": f"{name}"
                }
            }
        }

        results = self.es_client.search(index="personalities_finder", body=query)
        return [{'name': result["_source"]["title"], 'picture': result["_source"]["picture"]} for result in results["hits"]["hits"]][0]

if __name__ == "__main__":
    personalities = ElasticSearchPersonalities()
    
    #Add personalities:
    # personalities.add_personality_data('https://en.wikipedia.org/wiki/Albert_Einstein')
    # personalities.add_personality_data('https://en.wikipedia.org/wiki/Adolf_Hitler')
    # personalities.add_personality_data('https://en.wikipedia.org/wiki/Mahatma_Gandhi')
        
    #Run Query:
    # result = personalities.run_query("At what subjects was Einstein good in school?", "Albert Einstein", "heuristic")
    # print(result)

    #Delete Personality
    # personalities.remove_personality("Albert Einstein")
    # personalities.remove_personality("Adolf Hitler")
    # personalities.remove_personality("Mahatma Gandhi")
    personalities.remove_personality("Marie Curie")
    personalities.remove_personality("Alan Turing")
    personalities.remove_personality("Thomas Edison")
    
    #Get PErsonality
    # print(personalities.get_personality("Bagabond"))