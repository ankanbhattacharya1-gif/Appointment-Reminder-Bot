# Appointment-Reminder-Bot
Build a scheduling assistant that compresses appointment data and patient preferences, sending smart reminders efficiently
Build a scheduling assistant that compresses appointment data and patient preferences, sending smart reminders efficiently.

The Appointment Reminder Chatbot is a Python-based backend application developed using the FastAPI framework. The main goal of this project is to automate appointment scheduling and reminder notifications, reducing missed appointments and improving efficiency in healthcare and service-based systems. The chatbot allows users to book appointments either by providing structured data or by using natural language chat messages, making the system flexible and user-friendly.

The problem addressed by this project is the frequent occurrence of missed appointments due to forgetfulness or lack of timely reminders. Traditional manual systems are inefficient and prone to errors. This chatbot provides an automated solution that schedules appointments, stores patient preferences, and sends reminders when the appointment time approaches.

The system is built entirely using Python technologies. FastAPI is used to create RESTful APIs, SQLite is used as a lightweight database for storing appointment details, and Pydantic is used for validating user input. Uvicorn acts as the ASGI server that runs the application locally. No frontend or external services are required, making the project simple and lightweight.

When the application starts, it initializes the FastAPI server and creates an SQLite database named appointments.db if it does not already exist. The database contains a table that stores patient name, contact details, communication channel, appointment date and time, and user preferences. This ensures that all appointment information is stored persistently.

Users can schedule appointments in two ways. The first method uses a structured API endpoint where users provide appointment details such as date, time, contact information, and preferences. The second method allows users to book appointments using natural language chat messages like “Book me tomorrow at 3pm by SMS.” The chatbot parses the message to extract the appointment date, time, and communication channel automatically.

To improve efficiency, appointment details are compressed into a single formatted string that includes the patient name, communication channel, appointment time, and preferences. This compressed data format reduces storage complexity and makes it easier to process appointment records.

The reminder engine is a core component of the system. It periodically checks all stored appointments and identifies those scheduled within the next 24 hours. When an upcoming appointment is found, the system triggers a reminder. Currently, reminders are displayed in the terminal, and the system can easily be extended to send real email or SMS notifications.

The output of the system includes confirmation messages when appointments are successfully scheduled, compressed appointment data, and reminder notifications printed in the terminal. These outputs demonstrate that the chatbot is correctly parsing user input, storing data, and identifying upcoming appointments.

Overall, the Appointment Reminder Chatbot provides an effective and automated solution for managing appointments. It demonstrates the practical use of Python, FastAPI, and database management concepts. The project is suitable for real-world applications such as hospitals, clinics, salons, and educational institutions. Future enhancements can include SMS integration, WhatsApp notifications, web-based user interfaces, and improved natural language understanding.
