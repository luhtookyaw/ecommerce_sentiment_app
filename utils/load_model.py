from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained("luhtoo/bert-sentiment-olist")
model = BertForSequenceClassification.from_pretrained("luhtoo/bert-sentiment-olist")
model.eval()

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    pred = torch.argmax(probs, dim=1).item()
    label_map = {0: "negative", 1: "neutral", 2: "positive"}
    return label_map[pred]
