import sqlite3
import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(user='USERNAME', password='PASSWORD', host='HOST', database='DATABASE')
cursor = cnx.cursor()

# Function to create the database and tables
def create_database():
    # Connect to the database
    conn = sqlite3.connect('coaching_chatbot.db')
    c = conn.cursor()
    
    # Create the users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)''')
    
    # Create the tasks table
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, completed INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Create the habits table
    c.execute('''CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, frequency TEXT, completed INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to check if a user exists in the database
def user_exists(user_id):
    # Connect to the database
    conn = sqlite3.connect('coaching_chatbot.db')
    c = conn.cursor()
    
    # Retrieve the user from the database
    c.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user = c.fetchone()
    
    # Close the connection
    conn.close()
    
    # Return True if the user was found, False otherwise
    return user is not None

# Function to create a new user in the database
def create_user(user_id, username):
    # Connect to the database
    conn = sqlite3.connect('coaching_chatbot.db')
    c = conn.cursor()

    # Insert the new user into the database
    query = 'INSERT INTO users (id, username) VALUES (?, ?)'
    values = (user_id, username)
    c.execute(query, values)

    # Commit the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()

    # Update the task or habit in the database
    c.execute('UPDATE tasks SET completed=? WHERE id=?', (completed, task_or_habit_id))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to delete a task or habit from the database
def delete_task_or_habit(task_or_habit_id, task_or_habit):
    # Connect to the database
    conn = sqlite3.connect('coaching_chatbot.db')
    c = conn.cursor()
    
    # Delete the task or habit from the appropriate table
    if task_or_habit == 'task':
        c.execute('DELETE FROM tasks WHERE id=?', (task_or_habit_id,))
    elif task_or_habit == 'habit':
        c.execute('DELETE FROM habits WHERE id=?', (task_or_habit_id,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
