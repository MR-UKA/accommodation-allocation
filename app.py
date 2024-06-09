from flask import Flask, render_template, request, redirect, url_for
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder 
import pandas as pd 
app = Flask(__name__)

questions = [
    {"question": "Do you love people?", "options": ["Yes", "No", "Sometimes"]},
    {"question": "Are you hard to motivate?", "options": ["Yes", "No", "Sometimes"]},
    {"question": "Do you Avoid crisis?", "options": ["Yes", "No", "Sometimes"]},
    {"question": "Are you social?", "options": ["Yes", "No", "Sometimes"]},
    {"question": "Are you Talkative?", "options": ["Yes", "No", "Sometimes"]},
    {"question": "Are you Forgetful?", "options": ["Yes", "No", "Sometimes"]},
    {"question": "Do you consider yourself organized?", "options": ["Yes", "No", "Sometimes"]},
    {"question": "Are you Quick to judge?", "options": ["Yes", "No", "Sometimes"]},
    {"question": "Do you like to be alone?", "options": ["Yes", "No", "Sometimes"]},
    #{"question": "Do you like to exercise?", "options": ["Yes", "No", "Sometimes"]},
]

# Load machine learning model
#model = RandomForestClassifier()

#Load the model from the file
with open('personality.pkl', 'rb') as f:
    model = pickle.load(f)
#model.load("personality.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the user's answers
        answers = [request.form.get(question["question"]) for question in questions]

        # Predict personality using machine learning model
        personality = predict_personality(answers)

        # Render the template with the predicted personality
        return render_template("result.html", personality=personality)

    # Render the template with the questions
    return render_template("questions.html", questions=questions)

def predict_personality(answers):
    # Convert answers to numerical values
    le = LabelEncoder()
    answers = [le.fit_transform([answer])[0] for answer in answers]
    # Predict personality using machine learning model
    personality = model.predict([answers])[0]
    # Convert the predicted personality back to a string
    personality_labels = ["Sanguine", "Melancholy", "Choleric", "Phlegmatic"]
    personality = personality_labels[personality]
    return personality

if __name__ == "__main__":
    app.run(debug=True)