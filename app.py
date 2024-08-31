from flask import Flask, request, jsonify, render_template
import mysql.connector
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aman9097",
    database="museum"
)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    # Extracting parameters from Dialogflow's request
    intent = req.get("queryResult").get("intent").get("displayName")
    parameters = req.get("queryResult").get("parameters")
    
    response_text = ""

    if intent == "PreferredLanguageIntent":
        response_text = "What's your name?"

    elif intent == "NameIntent":
        name = parameters.get("name")
        response_text = "What is your sex (male/female/other)?"
        # Store name in session or database as needed

    elif intent == "SexIntent":
        sex = parameters.get("sex")
        response_text = "What is your age?"
        # Store sex in session or database as needed

    elif intent == "AgeIntent":
        age = parameters.get("age")
        response_text = "What is your nationality?"
        # Store age in session or database as needed

    elif intent == "NationalityIntent":
        nationality = parameters.get("nationality")
        response_text = "Please enter your Aadhaar or passport number."
        # Store nationality in session or database as needed

    elif intent == "AadhaarPassportNumberIntent":
        aadhaar_passport = parameters.get("aadhaar_passport_number")
        response_text = "How many people will be visiting?"
        # Store aadhaar/passport number in session or database as needed

    elif intent == "TotalNumberOfPeopleIntent":
        total_people = parameters.get("total_people")
        response_text = "Do you want the ticket to be sent to an email address? If yes, please enter your email; otherwise, type 'skip'."
        # Store total people in session or database as needed

    elif intent == "EmailIntent":
        email = parameters.get("email")
        if email.lower() == "skip":
            response_text = "Thank you! Your booking is complete."
        else:
            response_text = f"Thank you! The ticket will be sent to {email}."
            # Store email in session or database as needed

    # Assuming you've stored all the data in session or temporary variables, 
    # you can now store it in the database
    store_data_in_db(parameters)
    
    return jsonify({
        "fulfillmentText": response_text
    })

def store_data_in_db(parameters):
    cursor = db.cursor()
    sql = "INSERT INTO bookings (preferred_language, name, sex, age, nationality, aadhaar_passport, total_people, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        parameters.get("preferred_language"),
        parameters.get("name"),
        parameters.get("sex"),
        parameters.get("age"),
        parameters.get("nationality"),
        parameters.get("aadhaar_passport_number"),
        parameters.get("total_people"),
        parameters.get("email") if parameters.get("email").lower() != "skip" else None
    )
    cursor.execute(sql, values)
    db.commit()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
