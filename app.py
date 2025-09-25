from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# --- Database connection helper ---
def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        database=os.getenv("POSTGRES_DB", "mydb"),
        user=os.getenv("POSTGRES_USER", "rohit"),
        password=os.getenv("POSTGRES_PASSWORD", "mysecretpassword")
    )

# --- Routes ---
@app.route("/")
def home():
    return "Hello Rohit! 🚀 Your first Dockerized web app is running."

@app.route("/about")
def about():
    return "This is Rohit’s Dockerized Flask app!"

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/db-test")
def db_test():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
        return jsonify({"message": "Connected to Postgres! 🎉", "version": version})
    except Exception as e:
        return jsonify({"error": f"Database connection failed: {str(e)}"}), 500

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL
                    );
                """)
                cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
            conn.commit()
        return jsonify({"message": f"User {name} added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-users', methods=['GET'])
def get_users():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL
                    );
                """)
                cur.execute("SELECT id, name, email FROM users;")
                rows = cur.fetchall()
        user_list = [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
        return jsonify(user_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
        return jsonify({'message': f'User with ID {user_id} deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name and not email:
        return jsonify({"error": "At least one field (name or email) is required"}), 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if name and email:
                    cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s;", (name, email, user_id))
                elif name:
                    cur.execute("UPDATE users SET name = %s WHERE id = %s;", (name, user_id))
                elif email:
                    cur.execute("UPDATE users SET email = %s WHERE id = %s;", (email, user_id))
            conn.commit()
        return jsonify({"message": f"User with ID {user_id} updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Entry point ---
if __name__ == "__main__":
    print("Hello Rohit! Welcome to Docker.")
    print("Hello Rohit! Your container is running...")
    app.run(host="0.0.0.0", port=5000)