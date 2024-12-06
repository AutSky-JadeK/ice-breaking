import os
import torch
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification, Trainer

class TextDataset:
    def __init__(self, texts, tokenizer, max_length=512):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            max_length=self.max_length,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten()
        }

class SentimentClassifier:
    def __init__(self, model_dir='results/checkpoint-3560', model_name='bert-base-chinese'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_dir)
        self.trainer = Trainer(model=self.model, tokenizer=self.tokenizer)

    def get_score(self, texts):
        dataset = TextDataset(texts, self.tokenizer)
        predictions = self.trainer.predict(dataset)
        
        # 使用tanh函数将打分限制在[-1.0, 1.0]
        scores = np.tanh(predictions.predictions[:, 1] - predictions.predictions[:, 0])
        results = ['positive' if score > 0 else 'negative' for score in scores]
        
        return scores, results

# 示例使用
if __name__ == "__main__":
    classifier = SentimentClassifier()
    
    test_texts = [
        "这是一个非常好的产品。",
        "这个东西真是太糟糕了。",
        "我非常喜欢这个。",
        "我不喜欢这部电影。"
    ]
    
    scores, results = classifier.get_score(test_texts)
    for text, result in zip(test_texts, results):
        print(f"文本: {text} -> 结果: {result}")