import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch._utils")

from stageOne.getcontext import get_answer, load_data
# from stageTwo.dataloading import get_SSE_results, load_model_and_data
# from stageThree.new import response_generator
from time import time

def get_bot_response(query):
    start_time = time()

    # Load data and get the initial context from stage one
    stageOneModel, question_embeddings, questions, df = load_data()
    context = get_answer(query, stageOneModel, question_embeddings, questions, df)
    
    # # Proceed to stage two if no context is found in stage one
    # if context == 'not found':
    #     stageTwoModel, corpus_sentences, corpus_embeddings = load_model_and_data()
    #     context = get_SSE_results(query, stageTwoModel, corpus_sentences, corpus_embeddings)

    # Generate response based on the context obtained from stage one or two
    if context == 'not found':
        response = "Sorry, I do not have the answer to that. Please ask me another question."
    else:
        # Replace this with your actual response generation logic if needed
        # response = response_generator(query, context)
        response = "Temporary response data -- " + context

    # Debugging: Calculate and print the total processing time
    print('Total time:', round(time() - start_time, 4), 'seconds')

    return response
