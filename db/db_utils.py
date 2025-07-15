import psycopg2
import os

DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DB_URL, sslmode='require')

def fetch_next_question():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, question, options FROM questions WHERE used = FALSE ORDER BY random() LIMIT 1;")
    row = cur.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "question": row[1], "options": row[2]}
    return None

def mark_used(q_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE questions SET used = TRUE WHERE id = %s;", (q_id,))
    conn.commit()
    conn.close()

def get_used_questions_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM questions WHERE used = TRUE;")
    count = cur.fetchone()[0]
    conn.close()
    return count

if __name__ == "__main__":
    question = fetch_next_question()
    if question:
        print("Fetched question:", question)
    else:
        print("No unused questions found.")