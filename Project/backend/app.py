from elasticsearch_controller import ElasticSearchPersonalities
from download_personality_data import PersonalityData
from transformers import pipeline
from flask import Flask, request
from flask_cors import CORS
from urllib.parse import unquote_plus
import string
import torch

#Constants
models = { 
    "ALBERT XLARGE": "ktrapeznikov/albert-xlarge-v2-squad-v2",
    "ALBERT XXLARGE": "ahotrod/albert_xxlargev1_squad2_512",
    "BERT": "bert-large-uncased-whole-word-masking-finetuned-squad"
}

#Global Variables
indices = ["heuristic", "topics", "paragraphs", "phrases"]
model = "ALBERT XLARGE"
index = "heuristic"

#Flask Definitions
app = Flask(__name__)
CORS(app)

#Functions
def initialize_pipeline():
    global question_answering
    print(f"\nInitiating QA Pipeline with model {model}\n")
    question_answering = pipeline(task="question-answering", model=models[model], tokenizer=models[model], device=0)

def initialize_elasticsearch():
    global personalities
    print("\nStarting ElasticSearch\n")
    personalities = ElasticSearchPersonalities()

    
#Routes
@app.route("/")
def server_status():
    return "App is running."

@app.route("/api/model", methods=['GET','PUT'])
def model_interaction():
    global model
    if request.method == 'PUT':
        if 'model' in request.json:
            new_model = request.json['model']
            if new_model in models:
                model = new_model
                initialize_pipeline()
                return {"response": f"Model changed to {model}"}
            else:
                return{"error": "The requested model isn't available"}
        else:
            return {'error':"Request body didn't contain 'model'"}
    else:
        return {"response": f"{model}"}

@app.route("/api/models")
def get_models():
    return {'response': [key for key in models.keys()]}

@app.route("/api/index", methods=['GET','PUT'])
def index_interaction():
    global index
    if request.method == 'PUT':
        if 'index' in request.json:
            new_index = request.json['index']
            if new_index in indices:
                index = new_index
                print(f"Updated index to {index}")
                return {"response": f"Index changed to {index}"}
            else:
                return{"error": "The requested index isn't available"}
        else:
            return {'error':"Request body didn't contain 'index'"}
    else:
        return {"response": f"{index}"}

@app.route("/api/indices")
def get_indices():
    return {'response': indices}

@app.route("/api/finder")
def get_personalities():
    return {'response': personalities.get_finder()}

@app.route("/api/personality", methods=['POST'])
def add_personality():
    if 'url' in request.json:
        url = request.json['url']
        if url.startswith("https://en.wikipedia.org/wiki/"):
            personalities.add_personality_data(url)
            return {"response": "Personality Added"} 
        else:
            return {'error': "The URL given isn't a wikipedia page for this app"}
    else:
        return{'error': "Request body didn't contain 'url'"}

@app.route("/api/personality/<name>", methods=['GET'])
def get_figure(name):
    return {"response": personalities.get_personality(unquote_plus(name))}

@app.route("/api/question", methods=['POST'])
def ask_question():
    def check_full_message(data):
        for field in ["question", "name", "index"]:
            if field not in data:
                return False
        if data["index"] not in indices:
            return False
        if data["name"] not in [personality["name"] for personality in personalities.get_finder()]:
            return False
        return True
    
    data = request.json
    if(check_full_message(data)):
        context = personalities.run_query(data["question"], data["name"], data["index"])
        result = question_answering(context=context, question=data["question"], handle_impossible_answer=False)
        result = result["answer"].strip()
        torch.cuda.empty_cache()
        return {"response": result}
    else:
        return{"error": "Query Invalid"}

if __name__ == '__main__':
    initialize_elasticsearch()
    initialize_pipeline()
    print("App Sucessfully Started\n") 
    app.run(host="localhost", port=3000, debug=True)
