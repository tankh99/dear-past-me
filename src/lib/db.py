import sqlite3

# Initialize DB (run once)
def init_db():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory
                 (id INTEGER PRIMARY KEY, user TEXT, content TEXT)''')
    conn.commit()
    conn.close()

# Save a memory
def save_memory(user, content):
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("INSERT INTO memory (user, content) VALUES (?, ?)", (user, content))
    conn.commit()
    conn.close()

# Retrieve all memories for a user
def get_memories(user):
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("SELECT content FROM memory WHERE user=?", (user,))
    results = c.fetchall()
    conn.close()
    return [row[0] for row in results]