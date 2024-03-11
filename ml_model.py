import torch
from transformers import AutoConfig, AutoModelForSequenceClassification, BertTokenizer

model_ckpt = "models/URLTran-BERT-CLS-0"
config = AutoConfig.from_pretrained(model_ckpt)
config.num_labels = 2
config.problem_type = "single_label_classification"

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained(model_ckpt, config=config)

def predict(url):
    inputs = tokenizer(url, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).tolist()[0]
    return True if prediction == 1 else False