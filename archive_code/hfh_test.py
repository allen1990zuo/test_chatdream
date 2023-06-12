from transformers import AutoTokenizer, AutoModel

# Load the tokenizer and model for Sentence-BERT
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/bert-base-nli-mean-tokens")
model = AutoModel.from_pretrained("sentence-transformers/bert-base-nli-mean-tokens")

sentences = 'This is the first sentence.'
tokens = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
outputs = model(**tokens)
embeddings = outputs.last_hidden_state
print(embeddings.shape)
