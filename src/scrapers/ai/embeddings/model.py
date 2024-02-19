from transformers import AutoModelForCausalLM, AutoTokenizer

MISTRALAI_MODEL = 'mistralai/Mistral-7B-v0.1'
LITE_MODEL = 'distilgpt2'

model_id = LITE_MODEL
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Load the model and move it to GPU
model = AutoModelForCausalLM.from_pretrained(model_id).cuda()

text = 'Hello my name is Alexander and'
inputs = tokenizer(text, return_tensors='pt')

# Move the inputs to GPU
inputs = {k: v.cuda() for k, v in inputs.items()}

outputs = model.generate(**inputs, max_new_tokens=20)

# Move the outputs back to CPU for decoding
print(tokenizer.decode(outputs[0].cpu(), skip_special_tokens=True))
