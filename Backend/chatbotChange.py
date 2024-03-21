import os
import shutil

def chatbotChange(filename):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(BASE_DIR, 'UploadedFiles')
    target_dir = os.path.join(BASE_DIR, 'stageOne')

    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Define the source files based on the provided filename
    csv_or_excel_file = None
    pkl_file = None

    for f in os.listdir(source_dir):
        if f.startswith(filename) and (f.endswith('.csv') or f.endswith('.xlsx')):
            csv_or_excel_file = f
        elif f.startswith(filename) and f.endswith('.pkl'):
            pkl_file = f

    # Copy and rename the files if they exist
    if csv_or_excel_file:
        shutil.copy(os.path.join(source_dir, csv_or_excel_file), os.path.join(target_dir, 'questions_answers.csv'))
    if pkl_file:
        shutil.copy(os.path.join(source_dir, pkl_file), os.path.join(target_dir, 'question_embeddings.pkl'))

    return 'Files processed successfully' if csv_or_excel_file and pkl_file else 'Matching files not found'
