from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # <--- ADD THIS
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

if __name__ == '__main__':
    print("🚀 Starting Ek AASRA Flask Portal on http://127.0.0.1:5000")
    app.run(debug=True)
