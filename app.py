import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# --- Database Setup (SQLite) ---
def init_db():
    """Creates a local SQLite database to store volunteer entries if it doesn't exist."""
    conn = sqlite3.connect('volunteers.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            skills TEXT,
            availability TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when app starts
init_db()

# --- Route 1: Serve the Homepage ---
@app.route('/')
def home():
    """Serves the Ek AASRA frontend website."""
    return render_template('index.html')

# --- Route 2: Handle Volunteer Form Submissions ---
@app.route('/submit-volunteer', methods=['POST'])
def submit_volunteer():
    """Receives volunteer form data from the webpage and saves it using Python."""
    try:
        # Extract form data sent by user
        name = request.form.get('name')
        phone = request.form.get('phone')
        skills = request.form.get('skills')
        availability = request.form.get('availability')

        # Insert data into SQLite Database via Python
        conn = sqlite3.connect('volunteers.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO volunteers (name, phone, skills, availability)
            VALUES (?, ?, ?, ?)
        ''', (name, phone, skills, availability))
        conn.commit()
        conn.close()

        print(f"✅ [SUCCESS] New Volunteer Saved: {name} ({phone})")
        return jsonify({"status": "success", "message": "Thank you! Your volunteer application has been saved."}), 200

    except Exception as e:
        print(f"❌ [ERROR] Failed to save volunteer: {e}")
        return jsonify({"status": "error", "message": "An error occurred while saving your data."}), 500

# --- Route 3: Admin Endpoint to View Saved Volunteers ---
@app.route('/admin/volunteers', methods=['GET'])
def get_volunteers():
    """Returns all registered volunteers as JSON (Great for showing evaluators!)."""
    conn = sqlite3.connect('volunteers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, phone, skills, availability, submitted_at FROM volunteers')
    rows = cursor.fetchall()
    conn.close()

    # Format database rows into a clean list
    volunteers_list = []
    for row in rows:
        volunteers_list.append({
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "skills": row[3],
            "availability": row[4],
            "timestamp": row[5]
        })

    return jsonify({"total_volunteers": len(volunteers_list), "data": volunteers_list})
    # --- Route 4: Render Admin Dashboard Webpage ---
@app.route('/admin')
def admin_dashboard():
    """Renders the Admin Dashboard to view submitted volunteers in a table."""
    conn = sqlite3.connect('volunteers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, phone, skills, availability, submitted_at FROM volunteers ORDER BY submitted_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', volunteers=rows)

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
from google import genai  # Added for AI Assistant

app = Flask(__name__)
CORS(app)

# --- Initialize Gemini AI Client ---
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# NGO System Prompt - Restricts AI responses strictly to Ek Aasra
NGO_SYSTEM_INSTRUCTION = """
You are "Aasra AI", an empathetic and helpful AI assistant for Ek Aasra Welfare Society (an NGO dedicated to Animal and Human Welfare).

ABOUT EK AASRA:
- Mission: Dedicated to animal rescue, feeding drives, medical treatment, vaccination, and support for underprivileged communities.
- Key Services: Emergency animal rescues, daily feeding programs, community outreach, and volunteer engagement.
- Support: Visitors can donate or sponsor activities to keep operations running.

GUIDELINES:
1. Be warm, polite, and concise (2-4 sentences max per response).
2. For emergency animal rescues, immediately urge the user to check the Contacts section or call the emergency helpline directly.
3. If asked about non-NGO topics (like math or unrelated coding), gently redirect the conversation back to Ek Aasra's mission.
"""

# --- Database Setup (SQLite) ---
def init_db():
    """Creates a local SQLite database to store volunteer entries if it doesn't exist."""
    conn = sqlite3.connect('volunteers.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            skills TEXT,
            availability TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when app starts
init_db()

# --- Route 1: Serve the Homepage ---
@app.route('/')
def home():
    """Serves the Ek AASRA frontend website."""
    return render_template('index.html')

# --- Route 2: Handle Volunteer Form Submissions ---
@app.route('/submit-volunteer', methods=['POST'])
def submit_volunteer():
    """Receives volunteer form data from the webpage and saves it using Python."""
    try:
        # Extract form data sent by user
        name = request.form.get('name')
        phone = request.form.get('phone')
        skills = request.form.get('skills')
        availability = request.form.get('availability')

        # Insert data into SQLite Database via Python
        conn = sqlite3.connect('volunteers.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO volunteers (name, phone, skills, availability)
            VALUES (?, ?, ?, ?)
        ''', (name, phone, skills, availability))
        conn.commit()
        conn.close()

        print(f"✅ [SUCCESS] New Volunteer Saved: {name} ({phone})")
        return jsonify({"status": "success", "message": "Thank you! Your volunteer application has been saved."}), 200

    except Exception as e:
        print(f"❌ [ERROR] Failed to save volunteer: {e}")
        return jsonify({"status": "error", "message": "An error occurred while saving your data."}), 500

# --- Route 3: Admin Endpoint to View Saved Volunteers ---
@app.route('/admin/volunteers', methods=['GET'])
def get_volunteers():
    """Returns all registered volunteers as JSON (Great for showing evaluators!)."""
    conn = sqlite3.connect('volunteers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, phone, skills, availability, submitted_at FROM volunteers')
    rows = cursor.fetchall()
    conn.close()

    # Format database rows into a clean list
    volunteers_list = []
    for row in rows:
        volunteers_list.append({
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "skills": row[3],
            "availability": row[4],
            "timestamp": row[5]
        })

    return jsonify({"total_volunteers": len(volunteers_list), "data": volunteers_list})

# --- Route 4: Render Admin Dashboard Webpage ---
@app.route('/admin')
def admin_dashboard():
    """Renders the Admin Dashboard to view submitted volunteers in a table."""
    conn = sqlite3.connect('volunteers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, phone, skills, availability, submitted_at FROM volunteers ORDER BY submitted_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', volunteers=rows)

# --- Route 5: AI Assistant Endpoint ---
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handles incoming user queries and returns AI responses from Gemini."""
    data = request.json or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'response': 'Please enter a message.'}), 400

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config={
                'system_instruction': NGO_SYSTEM_INSTRUCTION
            }
        )
        return jsonify({'response': response.text})
    except Exception as e:
        print(f"❌ [ERROR] Chatbot failure: {e}")
        return jsonify({'response': 'Sorry, I am having trouble connecting right now.'}), 500
if __name__ == '__main__':
    # Read the PORT environment variable provided by Render (defaults to 5000 for local development)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


