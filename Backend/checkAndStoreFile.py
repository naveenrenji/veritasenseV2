import os
import pandas as pd
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer
import spacy
import pickle
import numpy as np

# spacy.cli.download("en_core_web_sm")
spacy_tokenizer = spacy.load('en_core_web_sm')
model = SentenceTransformer('all-MiniLM-L6-v2')

def save_obj(obj, name, directory):
    with open(os.path.join(directory, name + '.pkl'), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def checkAndStoreFile(file):
    # Check if the file is an Excel or CSV based on its extension
    if not (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
        return 'Error: The file must be either an Excel or CSV file.'

    # Attempt to read the file based on its extension
    try:
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)
    except Exception as e:
        return f'Error: Failed to read the file. {str(e)}'

    # Check if the dataframe contains exactly 2 columns named 'question' and 'answer'
    if len(df.columns) != 2 or not all(column in df.columns for column in ['question', 'answer']):
        return 'Error: The file must contain only 2 columns: "question" and "answer".'

    # If checks pass, save the file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(BASE_DIR, 'UploadedFiles')
    os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists
    save_path = os.path.join(save_dir, secure_filename(file.filename))

    try:
        file.seek(0)  # Move cursor back to beginning of file before saving
        file.save(save_path)
    except Exception as e:
        return f'Error: Could not save the file. {str(e)}'

    # Prepare data
    questions = [spacy_tokenizer(question).text for question in df['question']]
    question_embeddings = np.array(model.encode(questions, show_progress_bar=True))

    # Save the embeddings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(BASE_DIR, 'UploadedFiles')
    os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists

    try:
        filename_without_ext = os.path.splitext(secure_filename(file.filename))[0]
        save_obj(questions, f'{filename_without_ext}_questions', save_dir)
        save_obj(question_embeddings, f'{filename_without_ext}_embeddings', save_dir)
    except Exception as e:
        return f'Error: Could not save the file. {str(e)}'

    # If checks and processing pass, return success message
    return 'Success: File has been uploaded, processed, and stored.'

