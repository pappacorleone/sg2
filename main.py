import os
import telegram
import logging
from image_generator import generate_daily_summary_image, generate_weekly_summary_image
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from database import create_database, user_exists, create_user, get_tasks_and_habits, add_task_or_habit, get_task_or_habit, update_task_or_habit, delete_task_or_habit
from utils import is_adding_task, set_adding_task, clear_adding_task, is_adding_habit, set_adding_habit, clear_adding_habit, is_updating, set_updating, clear_updating, is_deleting, set_deleting, clear_deleting, is_selecting_status, set_selecting_status, clear_selecting_status, generate_daily_summary_image, generate_weekly_summary_image



import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the database if it doesn't exist ------------------------------
if not os.path.exists('coaching_chatbot.db'):
    create_database()

    # Initialize the bot ------------------------------
bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])
updater = Updater(bot=bot, use_context=True)

# Start the bot
def start(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Check if the user exists in the database
    if not user_exists(chat_id):
        # Add the user to the database
        create_user(chat_id, update.effective_user.first_name)
    
    # Send a greeting message
    context.bot.send_message(chat_id

# Add tasks command
def add_tasks(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the adding task flag in the user's session data
    set_adding_task(chat_id)
    
    # Send a message asking the user to enter the name of the task
    context.bot.send_message(chat_id, 'Please enter the name of the task:')

# Add habits command
def add_habits(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the adding habit flag in the user's session data
    set_adding_habit(chat_id)
    
    # Send a message asking the user to enter the name of the habit
    context.bot.send_message(chat_id, 'Please enter the name of the habit:')

# View tasks command
def view_tasks(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Retrieve the user's tasks and habits from the database
    tasks, habits = get_tasks_and_habits(chat_id)
    
    # Check if the user has any tasks
    if len(tasks) == 0:
        context.bot.send_message(chat_id, 'You have no tasks.')
    else:
        # Build the message
        message = 'Your tasks:\n'
        for task in tasks:
            # Check if the task is completed
            if task[3] == 1:
                completed = 'Completed'
            else:
                completed = 'Incomplete'
            message += '- {} ({})\n'.format(task[2], completed)
        
        # Send the message
        context.bot.send_message(chat_id, message)

            # View habits command
def view_habits(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Retrieve the user's tasks and habits from the database
    tasks, habits = get_tasks_and_habits(chat_id)
    
    # Check if the user has any habits
    if len(habits) == 0:
        context.bot.send_message(chat_id, 'You have no habits.')
    else:
        # Build the message
        message = 'Your habits:\n'
        for habit in habits:
            # Check if the habit is completed
            if habit[4] == 1:
                completed = 'Completed'
            else:
                completed = 'Incomplete'
            message += '- {} ({})\n'.format(habit[2], completed)
        
        # Send the message
        context.bot.send_message(chat_id, message)
# Add tasks command
def add_tasks(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the adding task flag in the user's session data
    set_adding_task(chat_id)
    
    # Send a message asking the user to enter the name of the task
    context.bot.send_message(chat_id, 'Please enter the name of the task:')

# Add habits command
def add_habits(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the adding habit flag in the user's session data
    set_adding_habit(chat_id)
    
    # Send a message asking the user to enter the name of the habit
    context.bot.send_message(chat_id, 'Please enter the name of the habit:')

# View tasks command
def view_tasks(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Retrieve the user's tasks and habits from the database
    tasks, habits = get_tasks_and_habits(chat_id)
    
    # Check if the user has any tasks
    if len(tasks) == 0:
        context.bot.send_message(chat_id, 'You have no tasks.')
    else:
        # Build the message
        message = 'Your tasks:\n'
        for task in tasks:
            # Check if the task is completed
            if task[3] == 1:
                completed = 'Completed'
            else:
                completed = 'Incomplete'
            message += '- {} ({})\n'.format(task[2], completed)
        
        # Send the message
        context.bot.send_message(
# Update tasks and habits command
def update(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the updating flag in the user's session data
    set_updating(chat_id)
    
    # Send a message asking the user to select the task or habit to update
    context.bot.send_message(chat_id, 'Please select the task or habit you want to update:', reply_markup=update_markup)

# Delete tasks and habits command
def delete(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the deleting flag in the user's session data
    set_deleting(chat_id)
    
    # Send a message asking the user to select the task or habit to delete
    context.bot.send_message(chat_id, 'Please select the task or habit you want to delete:', reply_markup=delete_markup)

# Message handler for tasks and habits
def task_or_habit_handler(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Check if the user is adding a task
    if is_adding_task(chat_id):
        # Clear the adding task flag in the user's session data
        clear_adding_task(chat_id)
        
        # Add the task to the database
        add_task_or_habit(chat_id, 'task', update.message.text)
        
        # Send a message confirming the task was added
        context.bot.send_message(chat_id, 'Task added!')
    
    # Check if the user is adding a habit
    elif is_adding_habit(chat_id):
        # Clear the adding habit flag in the user's session data
        clear_adding_habit(chat_id)
        
        # Add the habit to the database
        add_task_or_habit(chat_id, 'habit', update.message.text)
        
        # Set the selecting frequency flag in the user's session data
        set_selecting_frequency(chat_id)
        
        # Send a message asking the user to select the habit's frequency
        context.bot.send_message(chat_id, 'Please select the habit's frequency:', reply_markup=frequency_markup)
    
    # Check if the user is updating a task or habit
    elif is_updating(chat_id):
        # Clear the updating flag in the user's session data
        clear_updating(chat_id)
        
        # Get the task or habit id from the user's session data
        task_or_habit_id = context.user_data['task_or_habit_id']
        
        # Get the task or habit from the database
        task_or_habit = get_task_or_habit(

# Message handler for status updates
def status_update_handler(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Check if the user is selecting the status of a task or habit
    if is_selecting_status(chat_id):
        # Clear the selecting status flag in the user's session data
        clear_selecting_status(chat_id)
        
        # Get the task or habit id from the user's session data
        task_or_habit_id = context.user_data['task_or_habit_id']
        
        # Check if the user selected "Completed"
        if update.message.text == 'Completed':
            # Update the task or habit in the database
            update_task_or_habit(task_or_habit_id, completed=1)
            
            # Send a message confirming the update
            context.bot.send_message(chat_id, 'Task or habit marked as completed!')
        else:
            # Update the task or habit in the database
            update_task_or_habit(task_or_habit_id, completed=0)
            
            # Send a message confirming the update
            context.bot.send_message(chat_id, 'Task or habit marked as incomplete!')

# Message handler for all other messages
def message_handler(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Check if the user is deleting a task or habit
    if is_deleting(chat_id):
        # Clear the deleting flag in the user's session data
        clear_deleting(chat_id)
        
        # Get the task or habit id from the user's session data
        task_or_habit_id = context.user_data['task_or_habit_id']
        
        # Delete the task or habit from the database
        delete_task_or_habit(task_or_habit_id)
        
        # Send a message confirming the delete
        context.bot.send_message(chat_id, 'Task or habit deleted!')

        # Set the adding task flag in the user's session data ------------------    
def set_adding_task(chat_id):
    session_data = get_session_data(chat_id)
    session_data['adding_task'] = True
    set_session_data(chat_id, session_data)

# Clear the adding task flag in the user's session data
def clear_adding_task(chat_id):
    session_data = get_session_data(chat_id)
    del session_data['adding_task']
    set_session_data(chat_id, session_data)

# Check if the user is adding a task
def is_adding_task(chat_id):
    return 'adding_task' in get_session_data(chat_id)

# Set the adding habit flag in the user's session data
def set_adding_habit(chat_id):
    session_data = get_session_data(chat_id)
    session_data['adding_habit'] = True
    set_session_data(chat_id, session_data)

# Clear the adding habit flag in the user's session data
def clear_adding_habit(chat_id):
    session_data = get_session_data(chat_id)
    del session_data['adding_habit']
    set_session_data(chat_id, session_data)

# Check if the user is adding a habit
def is_adding_habit(chat_id):
    return 'adding_habit' in get_session_data(chat_id)

# Set the selecting frequency flag in the user's session data
def set_selecting_frequency(chat_id):
    session_data = get_session_data(chat_id)
    session_data['selecting_frequency'] = True
    set_session_data(chat_id, session_data)

# Clear the selecting frequency flag in the user's session data
def clear_selecting_frequency(chat_id):
    session_data = get_session_data(chat_id)
    del session_data['selecting_frequency']
    set_session_data(chat_id, session_data)

# Check if the user is selecting the frequency of a habit
def is_selecting_frequency(chat_id):
    return 'selecting_ -------------------------

# Set the updating flag in the user's session data
def set_updating(chat_id):
    session_data = get_session_data(chat_id)
    session_data['updating'] = True
    set_session_data(chat_id, session_data)

# Clear the updating flag in the user's session data
def clear_updating(chat_id):
    session_data = get_session_data(chat_id)
    del session_data['updating']
    set_session_data(chat_id, session_data)

# Check if the user is updating a task or habit
def is_updating(chat_id):
    return 'updating' in get_session_data(chat_id)

# Set the deleting flag in the user's session data
def set_deleting(chat_id):
    session_data = get_session_data(chat_id)
    session_data['deleting'] = True
    set_session_data(chat_id, session_data)

# Clear the deleting flag in the user's session data
def clear_deleting(chat_id):
    session_data = get_session_data(chat_id)
    del session_data['deleting']
    set_session_data(chat_id, session_data)

# Check if the user is deleting a task or habit
def is_deleting(chat_id):
    return 'deleting' in get_session_data(chat_id)

# Set the selecting status flag in the user's session data
def set_selecting_status(chat_id):
    session_data = get_session_data(chat_id)
    session_data['selecting_status'] = True
    set_session_data(chat_id, session_data)

# Clear the selecting status flag in the user's session data
def clear_selecting_status(chat_id):
    session_data = get_session_data(chat_id)
    del session_data['selecting_status']
    set_session_data(chat_id, session_data)

# Check if the user is selecting the status of a task or habit
def is_selecting_status(chat_id):
    return 'selecting_status' in get_session_data(chat_id)

# Start command
def start(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Send the start message
    context.bot.send_message(chat_id, 'Welcome to the motivational coaching chatbot! Use the /add_tasks and /add_habits commands to add tasks and habits, respectively. Use the /view_tasks and /view_habits commands to view your tasks and habits. Use the /update command to update a task or habit, and use the /delete command to delete a task or habit. Have a great day!')

# Add tasks command
def add_tasks(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the adding task flag in the user's session data
    set_adding_task(chat_id)
    
    # Send the prompt message
    context.bot.send_message(chat_id, 'Enter the tasks you want to add, separated by a comma:')

# Add habits command
def add_habits(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the adding habit flag in the user's session data
    set_adding_habit(chat_id)
    
    # Send the prompt message
    context.bot.send_message(chat_id, 'Enter the habits you want to add, separated by a comma:')

# View tasks command
def view_tasks(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Retrieve the user's tasks and habits from the database
    tasks, habits = get_tasks_and_habits(chat_id)
    
    # Check if the user has any tasks
    if len(tasks) == 0:
        context.bot.send_message(chat_id, 'You have no tasks.')
    else:
        # Build the message
        message = 'Your tasks:\n'
        for task in tasks:
            # Check if the task is completed
            if task[3] == 1:
                completed = 'Completed'
            else:
                completed = 'Incomplete'
            message += '- {} ({})\n'.format(task[2], completed)
        
        # Send the message
        context.bot.send_message(chat_id, message)

# View habits command
def view_habits(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Retrieve the user's tasks and habits from the database
    tasks, habits = get_tasks_and_habits(chat_id)
    
    # Check if the user has any habits
    if len(habits) == 0:
        context.bot.send_message(chat_id, 'You have no habits.')
    else:
        # Build the message
        message = 'Your habits:\n'
        for habit in habits:
            # Check if the habit is completed
            if habit[4] == 1:
                completed = 'Completed'
            else:
                completed = 'Incomplete'
            message += '- {} ({})\n'.format(habit[2], completed)
        
        # Send the message
        context.bot.send_message(chat_id, message)

# Update command
def update(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the updating flag in the user's session data
    set_updating(chat_id)
    
    # Send the prompt message
    context.bot.send_message(chat_id, 'What do you want to update? Enter the number of the task or habit you want to update:')

# Delete command
def delete(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Set the deleting flag in the user's session data
    set_deleting(chat_id)
    
    # Send the prompt message
    context.bot.send_message(chat_id, 'What do you want to delete? Enter the number of the task or habit you want to delete: ------------------
    # Message handler
def message_handler(update, context):
    # Get the user's chat id
    chat_id = update.effective_chat.id
    
    # Get the message text
    message_text = update.message.text
    
    # Check if the user is adding tasks
    if is_adding_task(chat_id):
        # Split the tasks into a list
        tasks = message_text.split(',')
        
        # Add the tasks to the database
        add_tasks_to_database(chat_id, tasks)
        
        # Clear the adding task flag in the user's session data
        clear_adding_task(chat_id)
        
        # Send the confirmation message
        context.bot.send_message(chat_id, 'Tasks added!')
    
    # Check if the user is adding habits
    elif is_adding_habit(chat_id):
        # Split the habits into a list
        habits = message_text.split(',')
        
        # Set the selecting frequency flag in the user's session data
        set_selecting_frequency(chat_id)
        
        # Send the prompt message
        context.bot.send_message(chat_id, 'Enter the frequency of each habit, separated by a comma:')
        
        # Store the habits in the user's session data
        set_session_data(chat_id, {'habits': habits})
    
    # Check if the user is selecting the frequency of habits
    elif is_selecting_frequency(chat_id):
        # Split the frequencies into a list
        frequencies = message_text.split(',')
        
        # Get the habits from the user's session data
        habits = get_session_data(chat_id)['habits']
        
        # Add the habits to the database
        add_habits_to_database(chat_id, habits, frequencies)
        
        # Clear the adding habit flag and the selecting frequency flag in the user's session data
        clear_adding_habit(chat_id)
        clear_selecting_frequency(chat_id)
        
        # Send the confirmation message
        context.bot.send_message(chat_id, 'Habits added!')
    
        # Check if the user is updating a task or habit
    elif is_updating(chat_id):
        # Check if the message text is a number
        if message_text.isdigit():
            # Convert the message text to an integer
            index = int(message_text)
            
            # Retrieve the user's tasks and habits from the database
            tasks, habits = get_tasks_and_habits(chat_id)
            
            # Check if the index is valid for the tasks
            if index > 0 and index <= len(tasks):
                # Set the task in the user's session data
                set_session_data(chat_id, {'task': tasks[index-1]})
                
                # Set the selecting status flag in the user's session data
                set_selecting_status(chat_id)
                
                # Send the prompt message
                context.bot.send_message(chat_id, 'Enter the new status of the task (completed/incomplete):')
            
            # Check if the index is valid for the habits
            elif index > len(tasks) and index <= len(tasks) + len(habits):
                # Set the habit in the user's session data
                set_session_data(chat_id, {'habit': habits[index-len(tasks)-1]})
                
                # Set the selecting status flag in the user's session data
                set_selecting_status(chat_id)
                
                # Send the prompt message
                context.bot.send_message(chat_id, 'Enter the new status of the habit (completed/incomplete):')
            
            # The index is invalid
            else:
                # Send the error message
                context.bot.send_message(chat_id, 'Invalid index.')
        
        # The message text is not a number
        else:
            # Send the error message
            context.bot.send_message(chat_id, 'Please enter a valid number.')
    
        # Check if the user is deleting a task or habit
    elif is_deleting(chat_id):
        # Check if the message text is a number
        if message_text.isdigit():
            # Convert the message text to an integer
            index = int(message_text)
            
            # Retrieve the user's tasks and habits from the database
            tasks, habits = get_tasks_and_habits(chat_id)
            
            # Check if the index is valid for the tasks
            if index > 0 and index <= len(tasks):
                # Delete the task from the database
                delete_task_from_database(chat_id, tasks[index-1][0])
                
                # Clear the deleting flag in the user's session data
                clear_deleting(chat_id)
                
                # Send the confirmation message
                context.bot.send_message(chat_id, 'Task deleted.')
            
            # Check if the index is valid for the habits
            elif index > len(tasks) and index <= len(tasks) + len(habits):
                # Delete the habit from the database
                delete_habit_from_database(chat_id, habits[index-len(tasks)-1][0])
                
                # Clear the deleting flag in the user's session data
                clear_deleting(chat_id)
                
                # Send the confirmation message
                context.bot.send_message(chat_id, 'Habit deleted.')
            
                        # The index is invalid
            else:
                # Send the error message
                context.bot.send_message(chat_id, 'Invalid index.')
        
        # The message text is not a number
        else:
            # Send the error message
            context.bot.send_message(chat_id, 'Please enter a valid number.')
    
    # Check if the user is selecting the status of a task or habit
    elif is_selecting_status(chat_id):
        # Get the task or habit from the user's session data
        task_or_habit = get_session_data(chat_id)['task_or_habit']
        
        # Check if the message text is 'completed' or 'incomplete'
        if message_text.lower() == 'completed' or message_text.lower() == 'incomplete':
            # Update the task or habit in the database
            update_task_or_habit_in_database(chat_id, task_or_habit, message_text.lower())
            
            # Clear the selecting status flag in the user's session data
            clear_selecting_status(chat_id)
            
            # Send the confirmation message
            context.bot.send_message(chat_id, 'Task or habit updated.')
        
        # The message text is invalid
        else:
            # Send the error message
            context.bot.send_message(chat_id, 'Please enter a valid status.')
    
    # The user is not adding, updating, or deleting a task or habit
    else:
        # Send the error message
        context.bot.send_message(chat_id, 'Invalid command.')

# Main function
def main():
    # Create the Updater and pass it the bot's token
    updater = Updater(TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Add the command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('add', add))
    dp.add_handler(CommandHandler('view_tasks', view_tasks))
    dp.add_handler(CommandHandler('view_habits', view_habits))
    dp.add_handler(CommandHandler('update', update))
    dp.add_handler(CommandHandler('delete', delete))
    
    # Add the message handler
    dp.add_handler(MessageHandler(Filters.text, message_handler))
    
        # Start the bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C
    updater.idle()

# Run the main function
if __name__ == '__main__':
    main()
---------------------

# Generate and send the weekly summary images for each user
for user in users:
    # Retrieve the user's tasks and habits from the database
    tasks, habits = get_tasks_and_habits(user['chat_id'])
    
    # Count the number of completed tasks and habits
    completed_tasks = sum([1 for task in tasks if task[1] == 'completed'])
    completed_habits = sum([1 for habit in habits if habit[1] == 'completed'])
    
    # Generate the weekly summary image
    generate_weekly_summary_image(user['chat_id'], completed_tasks, completed_habits, len(tasks), len(habits))
    
    # Send the weekly summary image to the user
    context.bot.send_photo(user['chat_id'], open(f'weekly_summary_{user['chat_id']}.png', 'rb'))


# Generate and send the daily summary images for each user
for user in users:
    # Retrieve the user's tasks and habits from the database
    tasks, habits = get_tasks_and_habits(user['chat_id'])
    
    # Count the number of completed tasks and habits
    completed_tasks = sum([1 for task in tasks if task[1] == 'completed'])
    completed_habits = sum([1 for habit in habits if habit[1] == 'completed'])
    
    # Generate the daily summary image
    generate_daily_summary_image(user['chat_id'], completed_tasks, completed_habits, len(tasks), len(habits))
    
    # Send the daily summary image to the user
    context.bot.send_photo(user['chat_id'], open(f'daily_summary_{user['chat_id']}.png', 'rb'))
    ------------------






# Add the command handlers
start_handler = CommandHandler('start', start)
add_tasks_handler = CommandHandler('add_tasks', add_tasks)
add_habits_handler = CommandHandler('add_habits', add_habits)
view_tasks_handler = CommandHandler('view_tasks', view_tasks)
view_habits_handler = CommandHandler('view_habits', view_habits)
update_handler = CommandHandler('update', update)
delete_handler = CommandHandler('delete', delete)
task_or_habit_handler = MessageHandler(Filters.text, task_or_habit_handler)
status_update_handler = MessageHandler(Filters.regex('^(Completed|Incomplete)$
# Add the error handler
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Add the command and message handlers to the dispatcher
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(add_tasks_handler)
updater.dispatcher.add_handler(add_habits_handler)
updater.dispatcher.add_handler(view_tasks_handler)
updater.dispatcher.add_handler(view_habits_handler)
updater.dispatcher.add_handler(update_handler)
updater.dispatcher.add_handler(delete_handler)
updater.dispatcher.add_handler(task_or_habit_handler)
updater.dispatcher.add_handler(status_update_handler)
updater.dispatcher.add_handler(message_handler)
updater.dispatcher.add_error_handler(error)

# Start the bot
updater.start_polling()
updater.idle()

------------------------------------------


# Initialize the bot and updater ------------------------------
bot = telegram.Bot(token='YOUR_BOT_TOKEN_HERE')
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher

# Define the handlers for different commands and messages
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

checklist_handler = CommandHandler('checklist', checklist)
dispatcher.add_handler(checklist_handler)

add_task_handler = CommandHandler('add_task', add_task)
dispatcher.add_handler(add_task_handler)

add_habit_handler = CommandHandler('add_habit', add_habit)
dispatcher.add_handler(add_habit_handler)

update_handler = CommandHandler('update', update)
dispatcher.add_handler(update_handler)

delete_handler = CommandHandler('delete', delete)
dispatcher.add_handler(delete_handler)

message_handler = MessageHandler(Filters.text, message)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
updater.idle()
