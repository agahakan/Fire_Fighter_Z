# app.py

# Import necessary libraries for Flask application
import os
from flask import Flask, request, jsonify  # Import libraries for Flask, HTTP requests and JSON responses
from flask_cors import CORS, cross_origin  # Import library for Cross-Origin Resource Sharing (CORS)
from firebase_admin import credentials, firestore, initialize_app  # Import libraries for Firebase Admin and Firestore
import json  # Import library for handling JSON data
import random  # Import library for generating random numbers

# Initialize Flask application
app = Flask(__name__)
# Enable CORS for the Flask application
cors = CORS(app)
# Set the header for CORS to "Content-Type"
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize Firestore database
# Load the certificate for accessing Firestore from 'server/key.json'
cred = credentials.Certificate('server/key.json')
# Initialize the Firebase Admin library using the certificate
default_app = initialize_app(cred)
# Connect to the Firestore database using the Firebase Admin library
db = firestore.client()
# Reference the 'cards' collection in the Firestore database
cards_ref = db.collection('cards')
# Reference the 'player' collection in the Firestore database
player_ref = db.collection('player')

@app.route('/adduser', methods=['POST'])
@cross_origin()
def addUser():
    try:
        # Get the username and password from the request parameters
        username = request.args.get('username')
        password = request.args.get('password')

        # Create a dictionary with the user information
        user_info = {
            "username": username,
            "password": password
        }
        print("user_info:", user_info)

        # Get a reference to the user document in Firestore
        user_ref = db.collection(username).document("userinfo")

        # Get the information for an existing user with the same username
        existing_user = user_ref.get().to_dict()
        
        # If a user with the same username already exists, return an error
        if existing_user:
            return jsonify({
                "status": "error",
                "message": "Username already exists"
            }), 409

        # Otherwise, add the new user information to Firestore
        user_ref.set(user_info)

        # Get a list of the user's documents in Firestore
        user_cards = [doc.to_dict() for doc in db.collection(username).stream()]
        
        # Create a dictionary with the response data
        response_data = {
            "status": "ok",
            "rc": user_cards
        }

        # Return the response data as a JSON object
        return jsonify(response_data), 200
    except Exception as e:
        # Return an error if there was a problem adding the user
        return f"An Error Occurred: {e}"


@app.route('/login', methods=['GET'])
@cross_origin()
def login():
    try:
        # Get the username and password from the request parameters
        username = request.args.get('username')
        password = request.args.get('password')

        # Create a dictionary with the user information
        user_info = {
            "username": username,
            "password": password
        }
        print("user_info:", user_info)

        # Get the information for an existing user with the same username
        existing_user = db.collection(username).document("userinfo").get().to_dict()
        print("existing_user:", existing_user)
        
        # If there is no user with the same username or the password is incorrect, return an error
        if not existing_user or existing_user["username"] != username or existing_user["password"] != password:
            return jsonify({
                "status": "error"
            }), 403
        
        # Add the "status" field to the user information with a value of "ok"
        existing_user["status"] = "ok"

        # Return the user information as a JSON object
        return jsonify(existing_user), 200
    except Exception as e:
        # Return an error if there was a problem logging in
        return f"An Error Occurred: {e}"



@app.route('/init', methods=['GET'])
@cross_origin()
def init():
    """
    init() : create cards and get 5 random cards
    This function initializes the game by creating the "cards" and "player" collections in the user's database, 
    and selecting 5 random cards to add to the "player" collection.
    """
    try:
        # Get the username from the query parameters in the request
        username = request.args.get('username')
        
        # Get the documents in the user's database as a list of dictionaries
        list_userdata = [doc.to_dict() for doc in db.collection(username).stream()]
        
        # Delete the existing "cards" document
        doc_cardref = db.collection(username).document("cards")
        doc = doc_cardref.get()
        if doc.exists:
            db.collection(username).document("cards").delete()

        # Delete all subcollections of the "cards" document
        for col in doc_cardref.collections():
            for doc in col.list_documents():
                doc.delete()

        # Load the contents of the "cards.json" file into the "cards" collection
        with open("cards.json", "r") as f:
            file_contents = json.load(f)
        db.collection(username).document("cards").set({})
        for c in file_contents:
            id = c["id"]
            db.collection(username).document("cards").collection(str(id)).document(str(id)).set(c)
        
        # Delete the existing "player" document
        doc_playerref = db.collection(username).document("player")
        doc = doc_playerref.get()
        if doc.exists:
            db.collection(username).document("player").delete()

        # Delete all subcollections of the "player" document
        for col in doc_playerref.collections():
            for doc in col.list_documents():
                doc.delete()

        # Create a new "player" document
        db.collection(username).document("player").set({})
        
        # Get a list of all the cards in the "cards" collection
        r_list = []
        list_cards = []
        for col in doc_cardref.collections():
            for doc in col.list_documents():
                list_cards.append(doc.get().to_dict())
        
        # Select 5 random cards and add them to the "player" collection
        for i in range(1, 6):
            val = random.choice(list_cards)
            while True:
                if val not in r_list:
                    id = str(val["id"])
                    r_list.append(val)
                    db.collection(username).document("player").collection(id).document(id).set(val)
                    db.collection(username).document("cards").collection(id).document(id).delete()
                    break
                else:
                    val = random.choice(list_cards)
        
        # Return the list of random cards
        return jsonify(r_list), 200
    except Exception as e:
        return f



# This function allows a user to draw one card randomly from the available cards.
# The drawn card is then added to the user's player card collection and removed from the available card collection.
# The function returns the drawn card in JSON format.
@app.route('/drawcard', methods=['GET'])
@cross_origin()
def drawcard():
    try:
        # Get the username from the query parameters
        username = request.args.get('username')

        # Get the references to the card and player collections
        doc_card_ref = db.collection(username).document("cards")
        player_ref = db.collection(username).document("player")

        # Get a list of all available cards
        card_collection_list = [col for col in doc_card_ref.collections()]
        cards = [doc.get().to_dict() for col in card_collection_list for doc in col.list_documents()]

        # If there are no cards available, return an error message
        if not cards:
            return jsonify({"status": "error", "message": "No cards available"}), 409
        
        # Choose a random card
        drawn_card = random.choice(cards)
        card_id = str(drawn_card["id"])

        # Add the drawn card to the player's collection and remove it from the available cards
        player_ref.collection(card_id).document(card_id).set(drawn_card)
        doc_card_ref.collection(card_id).document(card_id).delete()

        # Return the drawn card
        return jsonify(drawn_card), 200
    except Exception as e:
        # Return an error message if an exception occurs
        return f"An Error Occurred: {e}"


# This function retrieves a list of all cards from the "cards" collection of the user, chooses a random card from the list,
# adds it to the "player" collection of the user, deletes it from the "cards" collection of the user,
# and returns the list of all cards in the "player" collection of the user.
@app.route('/drawcards', methods=['GET'])
@cross_origin()
def drawcards():
    try:
        # Retrieve the username from the request arguments
        username = request.args.get('username')

        # Reference to the cards collection and player collection
        doc_cardref = db.collection(username).document("cards")
        doc_playerref = db.collection(username).document("player")

        # Store the list of cards in the cards collection
        list_cards=[]
        for col in doc_cardref.collections():
            for doc in col.list_documents():
                list_cards.append(doc.get().to_dict())
                
        # Select a random card from the list of cards
        my_card = random.choice(list_cards)
        id = str(my_card["id"])
        
        # Add the selected card to the player's collection and delete it from the cards collection
        db.collection(username).document("player").collection(id).document(id).set(my_card)
        db.collection(username).document("cards").collection(id).document(id).delete()
        
        # Store the list of cards in the player's collection
        list_player=[]
        for col in doc_playerref.collections():
            for doc in col.list_documents():
                list_player.append(doc.get().to_dict())
        
        # Return the list of cards in the player's collection to the client
        return jsonify(list_player), 200
    except Exception as e:
        # Return an error message if an exception occurs
        return f"An Error Occurred: {e}"


@app.route('/listcards', methods=['GET'])
@cross_origin()
def get_listcards():
    try:
        # Get the 'username' query parameter from the GET request
        username = request.args.get('username')
        
        # Access the document 'cards' in the Firestore collection with the same name as 'username'
        doc_cardref = db.collection(username).document("cards")
        
        # Initialize an empty list to store the card dictionaries
        list_cards = []
        
        # Loop through the sub-collections within the 'cards' document
        for col in doc_cardref.collections():
            # Loop through the documents in each sub-collection
            for doc in col.list_documents():
                # Append the dictionary representation of each document to the 'list_cards' list
                list_cards.append(doc.get().to_dict())
        
        # Return the 'list_cards' as a JSON object with a status code of 200 OK
        return jsonify(list_cards), 200
    except Exception as e:
        # Return an error message with the exception message if an exception occurs
        return f"An Error Occurred: {e}"


@app.route('/listplayercards', methods=['GET'])
@cross_origin()
def get_listplayercards():
    try:
        username = request.args.get('username')
        doc_playerref = db.collection(username).document("player")
        list_player=[]
        for col in doc_playerref.collections():
            #print(f'Deleting doc card {doc.id} => {doc.get().to_dict()}')
            for doc in col.list_documents():
                list_player.append(doc.get().to_dict())
        
        return jsonify(list_player), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/playcard', methods=['GET', 'PUT'])
@cross_origin()
def playcard():

    try:
        username = request.args.get('username')
        card_id = request.args.get('id')
        
        db.collection(username).document("player").collection(str(card_id)).document(str(card_id)).delete()
        
        doc_playerref = db.collection(username).document("player")
        list_player=[]
        for col in doc_playerref.collections():
            #print(f'Deleting doc card {doc.id} => {doc.get().to_dict()}')
            for doc in col.list_documents():
                list_player.append(doc.get().to_dict())
                
        return jsonify(list_player), 200
    except Exception as e:
        return f"An Error Occurred: {e}"
        

@app.route('/play_drawcard', methods=['GET', 'PUT'])
@cross_origin()
def play_drawcard():

    try:
        username = request.args.get('username')
        card_id = request.args.get('id')
        
        doc_cardref = db.collection(username).document("cards")
        doc_playerref = db.collection(username).document("player")
        
        db.collection(username).document("player").collection(str(card_id)).document(str(card_id)).delete()
        
        list_cards=[]
        for col in doc_cardref.collections():
            #print(f'Deleting doc card {doc.id} => {doc.get().to_dict()}')
            for doc in col.list_documents():
                list_cards.append(doc.get().to_dict())
                
        my_card = random.choice(list_cards)
        id = str(my_card["id"])
        db.collection(username).document("player").collection(id).document(id).set(my_card)
        db.collection(username).document("cards").collection(id).document(id).delete()
        
        doc_playerref = db.collection(username).document("player")
        list_player=[]
        for col in doc_playerref.collections():
            #print(f'Deleting doc card {doc.id} => {doc.get().to_dict()}')
            for doc in col.list_documents():
                list_player.append(doc.get().to_dict())
    

        return jsonify(list_player), 200
    except Exception as e:
        return f"An Error Occurred: {e}"
 

@app.route('/deletecard', methods=['GET', 'DELETE'])
@cross_origin()
def deletecard():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        card_id = request.args.get('id')
        username = request.args.get('username')
        
        db.collection(username).document("cards").collection(str(card_id)).document(str(card_id)).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"
        
@app.route('/deleteplayer', methods=['GET', 'DELETE'])
@cross_origin()
def deleteplayer():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        card_id = request.args.get('id')
        username = request.args.get('username')
        
        db.collection(username).document("player").collection(str(card_id)).document(str(card_id)).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)