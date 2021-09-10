from download_personality_data import PersonalityData
from transformers import pipeline
import pandas as pd
import torch
from openpyxl import load_workbook
from elasticsearch_controller import ElasticSearchPersonalities

print('Setting Parameters')
sheets = [0,1,2]
sheets_name = ['Albert Einstein', 'Adolf Hitler', 'Mahatma Gandhi']
URLs = ['https://en.wikipedia.org/wiki/Albert_Einstein', 'https://en.wikipedia.org/wiki/Adolf_Hitler', 'https://en.wikipedia.org/wiki/Mahatma_Gandhi']

#MODELS

# BERT / SQUAD v1: F1:93.15 EXACT:86.91
# question_answering = pipeline(task="question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad", tokenizer="bert-large-uncased-whole-word-masking-finetuned-squad", device=0)

# ALBERT XXLARGE / SQUAD v2: F1:89.35 EXACT:86.11
question_answering = pipeline(task="question-answering", model="ahotrod/albert_xxlargev1_squad2_512", tokenizer="ahotrod/albert_xxlargev1_squad2_512", device=0) 

# ALBERT XLARGE / SQUAD v2: F1:87.46 EXACT:84.41
# question_answering = pipeline(task="question-answering", model="ktrapeznikov/albert-xlarge-v2-squad-v2", tokenizer="ktrapeznikov/albert-xlarge-v2-squad-v2", device=0) 


answers_by = 'ALBERT XXLARGE - Heuristic Improved'

es_personalities = ElasticSearchPersonalities()

info = pd.read_excel('../../Question_Answers/Questions_and_Answers.xlsx', sheet_name=sheets, engine='openpyxl')
results=[]
for sheet in sheets:
    print(f'Getting Personality Data for personality #{sheet}')
    questions = [row for row in info[sheet]['Question']]

    result = []
    for index, question in enumerate(questions):
        print(f'Answering Question #{index}')
        context = es_personalities.run_query(question, sheets_name[sheet], "heuristic")
        result.append(question_answering(context=context, question=question, handle_impossible_answer=False))
        torch.cuda.empty_cache()
    
    results.append([one_result['answer'] for one_result in result])

writer = pd.ExcelWriter('./Questions_and_Answers.xlsx', engine='openpyxl') 

for sheet in sheets:
    info[sheet][f'Answers by {answers_by}'] = pd.DataFrame(results[sheet])
    info[sheet].to_excel(writer, sheets_name[sheet], index=False)

writer.save()