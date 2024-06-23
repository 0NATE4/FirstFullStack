import { useState } from "react";

const HTTP_OK = 200;
const HTTP_CREATED = 201;

const ContactForm = ({ existingContact = {}, updateCallBack }) => {
  const [firstName, setFirstName] = useState(existingContact.firstName || "");
  const [lastName, setLastName] = useState(existingContact.lastName || "");
  const [email, setEmail] = useState(existingContact.email || "");

  // Check if it already exists
  const updating = Object.entries(existingContact).length !== 0;

  const onSubmit = async (e) => {
   

    const data = {
      firstName,
      lastName,
      email,
    };

    const url =
      "http://127.0.0.1:5000/" +
      (updating ? `update_contact/${existingContact.id}` : "create_contact"); // Change URL based on whether update or creating
    // Setting options for request
    const options = {
      method: updating ? "PATCH" : "POST",
      headers: {
        "Content-Type": "application/json", //specifiy json
      },
      body: JSON.stringify(data),
    };
    const response = await fetch(url, options);
    if (response.status !== HTTP_CREATED && response.status !== HTTP_OK) {
      const data = await response.json();
      alert(data.message);
    } else {
      //success
    }
  };

  return (
    <form onSubmit={onSubmit}>
      <div>
        <label htmlFor="firstName">First Name:</label>
        <input
          type="text"
          id="firstName"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="lastName">Last Name:</label>
        <input
          type="text"
          id="lastName"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="text"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <button type="submit">{updating ? "Update" : "Create Contact"} </button>
    </form>
  );
};

export default ContactForm;
