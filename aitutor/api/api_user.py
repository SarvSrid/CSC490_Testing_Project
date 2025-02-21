from flask import Flask, Blueprint, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
user_blueprint = Blueprint('user', __name__)

# Database connection details
DB_HOST = "127.0.0.1"
DB_NAME = "test_db"
DB_USER = "postgres"
DB_PASS = "sharksnow"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@user_blueprint.route('/progress', methods=['GET'])
def get_progress():
    try:
        # Parse JSON from request payload
        data = request.get_json()
        userid = data.get('userid')

        if not userid:
            return jsonify({"error": "userid is required"}), 400

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Query the database for the user's progress
        cursor.execute("""
            SELECT l1_progress, l2_progress, l3_progress, l4_progress
            FROM user_progress
            WHERE userid = %s
        """, (userid,))

        user_progress = cursor.fetchone()

        # Close the database connection
        cursor.close()
        conn.close()

        if user_progress:
            return jsonify(user_progress), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.register_blueprint(user_blueprint)
    app.run(debug=True)