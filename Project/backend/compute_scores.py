import pandas as pd
import collections
import re
import string

class Get_Scores:

    def __init__(self, model, verbose = False):
        self.model = model
        self.verbose = verbose
        self.get_data_from_excel()
        self.calculate_scores()

    def get_tokens(self, s):
        if not s: return []
        return s.split()
    
    def compute_exact(self, a_gold, a_pred):
        return int(a_gold == a_pred)

    def compute_f1(self, a_gold, a_pred):
        gold_toks = self.get_tokens(a_gold)
        pred_toks = self.get_tokens(a_pred)
        common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
        num_same = sum(common.values())
        if len(gold_toks) == 0 or len(pred_toks) == 0:
            # If either is no-answer, then F1 is 1 if they agree, 0 otherwise
            return int(gold_toks == pred_toks)
        if num_same == 0:
            return 0
        precision = 1.0 * num_same / len(pred_toks)
        recall = 1.0 * num_same / len(gold_toks)
        f1 = (2 * precision * recall) / (precision + recall)
        return f1

    def normalize_answer(self, s):
        """Lower text and remove punctuation, articles and extra whitespace."""
        def remove_articles(text):
            regex = re.compile(r'\b(a|an|the)\b', re.UNICODE)
            return re.sub(regex, ' ', text)
        def white_space_fix(text):
            return ' '.join(text.split())
        def remove_punc(text):
            exclude = set(string.punctuation)
            return ''.join(ch for ch in text if ch not in exclude)
        def lower(text):
            return text.lower()
        return white_space_fix(remove_articles(remove_punc(lower(s))))    

    def get_raw_scores(self, golds, preds):
        exact_scores = []
        f1_scores = []
        for i in range(len(golds)):
            gold_answers = [self.normalize_answer(golds[i])]
            pred_answers = [self.normalize_answer(preds[i])]
            if self.verbose:
                print(set(zip(gold_answers, pred_answers)))
            for a_gold, a_pred in zip(gold_answers, pred_answers):   
                exact_scores.append(self.compute_exact(a_gold, a_pred))
                f1_scores.append(self.compute_f1(a_gold, a_pred))

        self.raw_exact = exact_scores
        self.raw_f1 = f1_scores
    
    def get_data_from_excel(self):
        sheets = [0,1,2]
        # sheets_name = ['Albert Einstein', 'Adolf Hitler', 'Mahatma Gandhi']
        # URLs = ['https://en.wikipedia.org/wiki/Albert_Einstein', 'https://en.wikipedia.org/wiki/Adolf_Hitler', 'https://en.wikipedia.org/wiki/Mahatma_Gandhi']


        info = pd.read_excel('../../Question_Answers/Questions_and_Answers.xlsx', sheet_name=sheets, engine='openpyxl')
        self.questions = []
        self.gold_answers = []
        self.predicted_answers = []

        for sheet in sheets:
            self.questions.extend(list(info[sheet]['Question']))
            self.gold_answers.extend(list(info[sheet]['Answer']))
            self.predicted_answers.extend(list(info[sheet][self.model]))
    
    def calculate_scores(self):
        self.get_raw_scores(self.gold_answers, self.predicted_answers)
        self.exact_score = 100 * sum(self.raw_exact)/len(self.raw_exact)
        self.f1_score = 100 * sum(self.raw_f1)/len(self.raw_f1)


if __name__ == '__main__':
    models = ["Answers by BERT - Heuristic", "Answers by ALBERT XLARGE - Heuristic", "Answers by ALBERT XXLARGE - Heuristic", "Answers by BERT - Heuristic Improved", "Answers by ALBERT XLARGE - Heuristic Improved", "Answers by ALBERT XXLARGE - Heuristic Improved"]
    for model in models:
        scores = Get_Scores(model)
        print(f"Scores for {scores.model}")
        print(f"F1 Score: {scores.f1_score}")
        print(f"Exact Score: {scores.exact_score}")
        print('\n\n')
