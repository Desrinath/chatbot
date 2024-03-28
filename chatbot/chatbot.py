from flask import Flask, render_template, request
import random

app = Flask(__name__)

def load_dataset(file_path):
    """Load dataset from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        conversations = file.readlines()
    return [conversation.strip() for conversation in conversations]

def train_chatbot(human_dataset, bot_dataset):
    """Train the chatbot using the provided datasets."""
    chatbot_data = {}
    for human_query, bot_response in zip(human_dataset, bot_dataset):
        if human_query not in chatbot_data:
            chatbot_data[human_query] = []
        chatbot_data[human_query].append(bot_response)
    return chatbot_data

def suggest_random_questions(dataset):
    """Suggest random questions from the dataset."""
    random_questions = random.sample(dataset, min(3, len(dataset)))
    return random_questions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input'].strip().lower()
    if user_input == 'exit':
        response = "Goodbye!"
    elif user_input in chatbot_data:
        response = random.choice(chatbot_data[user_input])
    else:
        response = "I'm sorry, I don't understand that."
    
    random_questions = suggest_random_questions(human_dataset)
    
    return {
        'response': response,
        'random_questions': random_questions
    }

if __name__ == '__main__':
    # Path to your human and bot dataset files
    human_dataset_file_path = 'human_text.txt'
    bot_dataset_file_path = 'robot_text.txt'

    # Load datasets
    human_dataset = load_dataset(human_dataset_file_path)
    bot_dataset = load_dataset(bot_dataset_file_path)

    # Train chatbot
    chatbot_data = train_chatbot(human_dataset, bot_dataset)

    app.run(debug=True)
