from sentence_transformers import SentenceTransformer

model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)
model.save('./models/all-MiniLM-L6-v2')
