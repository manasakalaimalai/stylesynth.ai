from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import dotenv_values
import gpt4all
import requests
import base64
import os
 
config = dotenv_values(".env")
api_host = config["API_HOST"]
api_key = config["STABE_DIFFUSION_API_KEY"]
engine_id = config["ENGINE_ID"]

app = Flask(__name__)
CORS(app)


@app.route("/generate", methods=["GET"])
def generate():

    # This will download gpt4all-j v1.3 groovy model, which is ~3.7GB
    gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")

    # We create 2 prompts, one for the description and then another one for the name of the product
    prompt_description = 'You are a business consultant. Please write a short description for a product idea for an online shop inspired by the following concept: "' + \
        request.args.get(
            "prompt") + '"'
    messages_description = [{"role": "user", "content": prompt_description}]
    description = gptj.chat_completion(messages_description)[
        'choices'][0]['message']['content']

    prompt_name = 'You are a business consultant. Please write a name of maximum 5 words for a product with the following description: "' + description + '"'
    messages_name = [{"role": "user", "content": prompt_name}]
    name = gptj.chat_completion(messages_name)[
        'choices'][0]['message']['content']

    image_path = generateImage(name)
    result = {"name": name, "description": description, "image": image_path}

    return jsonify(result)


# def check_and_create_filename(filename):
#     base_name, extension = os.path.splitext(filename)
#     counter = 1
#     new_filename = filename

#     while os.path.exists(new_filename):
#         new_filename = f"{base_name}_{counter}{extension}"
#         counter += 1

#     return new_filename

def main():
    app.run(host="localhost", port=8000)
    print("Server running on  port 8000")


if __name__ == "__main__":
    main()