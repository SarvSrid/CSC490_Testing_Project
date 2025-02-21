from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

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

@app.route('/validate_quiz', methods=['POST'])
def validate_quiz():
    try:
        # Parse JSON from request payload
        data = request.get_json()
        userid = data.get('userid')
        question_number = data.get('question_number')
        selected_answer = data.get('selected_answer')

        if not userid or not question_number or not selected_answer:
            return jsonify({"error": "userid, question_number, and selected_answer are required"}), 400

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Query the database for the correct answer
        cursor.execute("""
            SELECT correct_answer
            FROM quiz_questions
            WHERE question_number = %s
        """, (question_number,))

        correct_answer = cursor.fetchone()

        if not correct_answer:
            cursor.close()
            conn.close()
            return jsonify({"error": "Question not found"}), 404

        # Check if the selected answer is correct
        if selected_answer == correct_answer['correct_answer']:
            # Increment the user's progress
            cursor.execute("""
                UPDATE user_progress
                SET l{}_progress = l{}_progress + 1
                WHERE userid = %s
            """.format(question_number, question_number), (userid,))

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "Correct answer"}), 200
        else:
            cursor.close()
            conn.close()
            return jsonify({"message": "Incorrect answer"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=6001)