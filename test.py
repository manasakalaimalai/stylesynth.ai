from gpt4all import GPT4All
model = GPT4All("llama-2-7b-chat.ggmlv3.q4_0.bin")
output = model.generate("Reply like you're a fashion assistant, I need a concise and straightforward answer, only listing the names of the clothes required. Suggest an appropriate outfit for Christmas party.", max_tokens=20)
print(output)