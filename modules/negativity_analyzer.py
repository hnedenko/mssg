from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F


class NegativityAnalyser:

    def __init__(self):
        # Замените 'model_name' на реальное имя многоязычной модели тональности с HF
        # (например, для демонстрации используем условное имя)
        MODEL_NAME = "camiloajt/xlmr-sentiment-es"
        # Ваша реальная модель должна быть проверена на работу с RU/UK

        # Загрузка токенизатора и модели
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}. Проверьте имя модели.")
            exit()

        self.device = torch.device("cpu")

        self.model.to(self.device)
        self.model.eval()

    def is_article_negativity(self, article, threshold):

        # generate text tonality
        inputs = self.tokenizer(
            article.origin_text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits[0]

        probabilities = F.softmax(logits, dim=0).cpu().numpy()

        result = (float(probabilities[0]), float(probabilities[1]), float(probabilities[2]))

        # check "positivity" by threshold
        if result[0] - result[2] > threshold:
            return True
        else:
            return False
