from flask import request, jsonify
from config import app, db
from models import Contact

# Get method decorater, so only GET
@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all() # Gets all the contacts in the db

    # Convert contacts from python data to json
    json_contacts = list(map(lambda x: x.json().to_json(), contacts))
    return jsonify({"contacts": json_contacts})

# Only Post, creating contact
@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    # Now check if those values exist
    if not first_name or not last_name or not email:
        return jsonify(
            {"message:" "You must include a first name, last name and email"}
        ), 400

    # Create Contact
    new_contact = Contact(first_name=first_name, 
                          last_name=last_name, 
                          email=email)
    try:
        db.session.add(new_contact)
        db.session.commit() # Write into the database
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    # Successful
    return jsonify({"message": "User created!"}), 201

# Patch, Updates contact if it exists
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json

    # If first name exists, update, otherwise use pre existing one
    contact.first_name = data.get("firstName", contact.first_name)
    # Same for last name and email
    contact.first_name = data.get("lastName", contact.last_name)
    contact.first_name = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User updated!"}), 200

# Delete, Deletes user if it exists
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all() # If database doesn't exist, create it

    app.run(debug=True)