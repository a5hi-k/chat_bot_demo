from flask import Flask
from flask import render_template,request,jsonify
import os
import google.generativeai as genai
import json
from difflib import get_close_matches




app=Flask(__name__ ,template_folder='templates')
app.app_context().push()





genai.configure(api_key=os.environ["GEMINI_API_KEY"])


generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 2048,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.0-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
)



def read_file_to_dict(file_path):
    data_dict = {
        "role": "user",
        "parts": []
    }
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            data_dict["parts"].append(file_content)
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data_dict


file_path = 'store_data.txt'
result = read_file_to_dict(file_path)



chat_session = model.start_chat(
  history=[
    result,
    {
      "role": "model",
      "parts": [
        "--- END OF FILE store_data.txt ---",
      ],
    }    
  ]
)

# response = chat_session.send_message("INSERT_INPUT_HERE")


# print(chat_session.history)

def get_bot_response_for_llm(message):

    response = chat_session.send_message(message)
    return response.text





# CODE FOR THE NORMAL CHAT BOT

def chat_load(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        data: dict = json.load(f)
    return data    

def chat_save(file_path: str, data: dict):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def best_match(user_question, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=2, cutoff=0.6) 
    return matches[0] if matches else None       

def get_answer(question: str, chat: dict) -> str | None:
    for q in chat['questions']:
        if q['question'] == question:
          return q['answer']
        




def get_bot_response_for_normal(message):

    chat: dict = chat_load('chat.json')

    best_m: str | None = best_match(message, [q['question'] for q in chat['questions']])

    if best_match:
        answer: str = get_answer(best_m, chat)

        if answer:

          return answer
        else:
            return "Sorry, I didn't understand that."
    else:
        return "Sorry, I didn't understand that. Can you please rephrase?"



@app.route("/", methods=["GET"])
def home():
    return render_template('home.html')



@app.route('/chat1', methods=['POST'])
def chat1():
    user_message = request.json.get('message')
    bot_response = get_bot_response_for_llm(user_message)
    return jsonify(response=bot_response)



@app.route('/chat2', methods=['POST'])
def chat2():
    user_message = request.json.get('message')
    bot_response = get_bot_response_for_normal(user_message)
    return jsonify(response=bot_response)





