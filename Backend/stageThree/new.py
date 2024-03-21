from torch import cuda, bfloat16
import transformers
from transformers import StoppingCriteria, StoppingCriteriaList

from huggingface_hub import login
import logging
import torch

auth_token = "auth"
login(auth_token)
logging.getLogger().setLevel(logging.ERROR)


model_id = 'meta-llama/Llama-2-7b-chat-hf'

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

# set quantization configuration to load large model with less GPU memory
# this requires the `bitsandbytes` library
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

# begin initializing HF items, you need an access token
hf_auth = 'auth'
model_config = transformers.AutoConfig.from_pretrained(
    model_id,
    token=hf_auth
)


model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    quantization_config=bnb_config,
    device_map='auto',
    token=hf_auth
)

# enable evaluation mode to allow model inference
model.eval()

print(f"Model loaded on {device}")

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id,
    token=hf_auth
)


stop_list = ['\nHuman:', '\n```\n', '\nSpeaker:']

stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]

# define custom stopping criteria object
class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_ids in stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False

stopping_criteria = StoppingCriteriaList([StopOnTokens()])

generate_text = transformers.pipeline(
    model=model, 
    tokenizer=tokenizer,
    return_full_text=True,  # langchain expects the full text
    task='text-generation',
    # we pass model parameters here too
    stopping_criteria=stopping_criteria,  # without this model rambles during chat
    temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
    max_new_tokens=512,  # max number of tokens to generate in the output
    repetition_penalty=1.1  # without this output begins repeating
)


def response_generator(question, context):
    res = generate_text(f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context -")
    generated_text = res[0]["generated_text"]
     # Find the index of "now respond-" and slice the text from that point forward
    respond_index = generated_text.find("now respond based on the context -")
    if respond_index != -1:
        # Add the length of "now respond-" to start after this substring
        start_index = respond_index + len("now respond based on the context -")
        return generated_text[start_index:].strip()  # Strip to remove any leading/trailing whitespace
    else:
        # If "now respond-" is not found, return the entire generated text
        return generated_text

# question = "What is AI?"
# context = "Artificial Intelligence is a field of computer science."
# response = response_generator(question, context)
# print(response)
