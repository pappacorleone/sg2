import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import database
import utils

# Function to handle the '/start' command
def start(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.first_name
    
    # Check if the user is already in the database
    if not database.user_exists(user_id):
        # If not, create a new user in the database
        database.create_user(user_id, username)
    
    # Create the main menu keyboard
    main_menu_keyboard = [['My checklist', 'Add task', 'Add habit'],
                         ['Update task/habit', 'Delete task/habit', 'Infographic summary']]
    main_menu_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    # Send the main menu to the user
    update.message.reply_text(text='Welcome to the motivational coaching chatbot, {}!\n\nPlease select an option from the menu below:'.format(username), reply_markup=main_menu_markup)

# Function to handle the '/checklist' command
def checklist(update, context):
    user_id = update.effective_user.id
    
    # Retrieve the user's tasks and habits from the database
    tasks, habits = database.get_tasks_and_habits(user_id)
    
    # Format the tasks and habits into a message
    message = '*Tasks:*\n'
    for task in tasks:
        task_id, task_name, task_completed = task
        if task_completed:
            message += '- {} (completed)\n'.format(task_name)
        else:
            message += '- {} (in progress)\n'.format(task_name)
    message += '\n*Habits:*\n'
    for habit in habits:
        habit_id, habit_name, habit_frequency, habit_completed = habit
        if habit_completed:
            message += '- {} (completed {} times)\n'.format(habit_name, habit_completed)
        else:
            message += '- {} (in progress, {} times completed)\n'.format(habit_name, habit_completed)
    
    # Send the message to the user
    update.message.reply_text(text=message, parse_mode='Markdown')

# Function to handle the '/add_task' command
def add_task(update, context):
    user_id = update.effective_user.id
    
    # Send the message asking the user to enter the name of the task
    update.message.reply_text(text='Please enter the name of the task:')

# Function to handle the '/add_habit' command
def add_habit(update, context):
    user_id = update.effective_user.id
    
    # Create the keyboard for selecting the frequency
    frequency_keyboard = [['Daily', 'Weekly']]
    frequency_markup = telegram.ReplyKeyboardMarkup(frequency_keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    # Send the message asking the user to enter the name and frequency of the habit
    update.message.reply_text(text='Please enter the name and frequency of the habit:', reply_markup=frequency_markup)

# Function to handle the '/update' command
def update(update, context):
    user_id = update.effective_user.id
    
    # Retrieve the user's tasks and habits from the database
    tasks, habits = database.get_tasks_and_habits(user_id)
    
    # Create the keyboard for selecting the task or habit to update
    update_keyboard = []
    for task in tasks:
        task_id, task_name, task_completed = task
        update_keyboard.append(['Task: {}'.format(task_name)])
    for habit in habits:
        habit_id, habit_name, habit_frequency, habit_completed = habit
        update_keyboard.append(['Habit: {}'.format(habit_name)])
    update_markup = telegram.ReplyKeyboardMarkup(update_keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    # Send the message asking the user to select the task or habit to update
    update.message.reply_text(text='Please select the task or habit you want to update:', reply_markup=update_markup)

# Function to handle the '/delete' command
def delete(update, context):
    user_id = update.effective_user.id
    
    # Retrieve the user's tasks and habits from the database
    tasks, habits = database.get_tasks_and_habits(user_id)
    
    # Create the keyboard for selecting the task or habit to delete
    delete_keyboard = []
    for task in tasks:
        task_id, task_name, task_completed = task
        delete_keyboard.append(['Task: {}'.format(task_name)])
    for habit in habits:
        habit_id, habit_name, habit_frequency, habit_completed = habit
        delete_keyboard.append(['Habit: {}'.format(habit_name)])
    delete_markup = telegram.ReplyKeyboardMarkup(delete_keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    # Send the message asking the user to select the task or habit to delete
    update.message.reply_text(text='Please select the task or habit you want to delete:', reply_markup=delete_markup)

# Function to handle incoming text messages
def message(update, context):
    user_id = update.effective_user.id
    message = update.message.text
    
    # Check if the user is in the process of adding a task
    if utils.is_adding_task(user_id):
        # Add the task to the database
        database.add_task_or_habit(user_id, message, 'task', None)
        
        # Clear the adding task flag
        utils.clear_adding_task(user_id)
        
        # Send the confirmation message
        update.message.reply_text(text='Task added successfully!')
        
        # Return to the main menu
        start(update, context)
    
    # Check if the user is in the process of adding a habit
    elif utils.is_adding_habit(user_id):
        # Split the message into the habit name and frequency
        habit_name, habit_frequency = message.split(' ')
        
        # Add the habit to the database
        database.add_task_or_habit(user_id, habit_name, 'habit', habit_frequency)
        
        # Clear the adding habit flag
        utils.clear_adding_habit(user_id)
        
        # Send the confirmation message
        update.message.reply_text(text='Habit added successfully!')
        
        # Return to the main menu
        start(update, context)
    
    # Check if the user is in the process of updating a task or habit
    elif utils.is_updating(user_id):
        # Split the message into the task or habit type and name
        task_or_habit_type, task_or_habit_name = message.split(': ')
        
        # Retrieve the task or habit from the database
        if task_or_habit_type == 'Task':
            task_or_habit = database.get_task_or_habit(task_or_habit_name, 'task')
        elif task_or_habit_type == 'Habit':
            task_or_habit = database.get_task_or_habit(task_or_habit_name, 'habit')
        
        # Check if the task or habit was found in the database
        if task_or_habit:
            task_or_habit_id, task_or_habit_name, task
            # Create the keyboard for selecting the status of the task or habit
            status_keyboard = [['Completed', 'In progress']]
            status_markup = telegram.ReplyKeyboardMarkup(status_keyboard, one_time_keyboard=True, resize_keyboard=True)
            
            # Send the message asking the user to select the status of the task or habit
            update.message.reply_text(text='Please select the status of the {}:'.format(task_or_habit_type), reply_markup=status_markup)
        else:
            # Send the error message
            update.message.reply_text(text='Task or habit not found! Please try again.')
            
            # Clear the updating flag
            utils.clear_updating(user_id)
            
            # Return to the main menu
            start(update, context)
    
    # Check if the user is in the process of deleting a task or habit
    elif utils.is_deleting(user_id):
        # Split the message into the task or habit type and name
        task_or_habit_type, task_or_habit_name = message.split(': ')
        
        # Retrieve the task or habit from the database
        if task_or_habit_type == 'Task':
            task_or_habit = database.get_task_or_habit(task_or_habit_name, 'task')
        elif task_or_habit_type == 'Habit':
            task_or_habit = database.get_task_or_habit(task_or_habit_name, 'habit')
        
        # Check if the task or habit was found in the database
        if task_or_habit:
            task_or_habit_id, task_or_habit_name, task_or_habit_completed = task_or_habit
            
            # Delete the task or habit from the database
            database.delete_task_or_habit(task_or_habit_id, task_or_habit_type.lower())
            
            # Clear the deleting flag
            utils.clear_deleting(user_id)
            
            # Send the confirmation message
            update.message.reply_text(text='{} deleted successfully!'.format(task_or_habit_type))
            
            # Return---------------------------------------------------------------------------

            # Send the error message
            update.message.reply_text(text='Task or habit not found! Please try again.')
            
            # Clear the deleting flag
            utils.clear_deleting(user_id)
            
            # Return to the main menu
            start(update, context)
    
    # Check if the user is in the process of selecting the status of a task or habit
    elif utils.is_selecting_status(user_id):
        # Split the message into the task or habit type and status
        task_or_habit_type, task_or_habit_status = message.split(': ')
        
        # Get the task or habit ID from the session data
        task_or_habit_id = context.user_data['task_or_habit_id']
        
        # Update the task or habit in the database
        database.update_task_or_habit(task_or_habit_id, task_or_habit_status.lower())
        
        # Clear the selecting status flag
        utils.clear_selecting_status(user_id)
        
        # Send the confirmation message
        update.message.reply_text(text='{} status updated successfully!'.format(task_or_habit_type))
        
        # Return to the main menu
        start(update, context)
    
    # If none of the above conditions are met, the user has entered an invalid command or message
    else:
        update.message.reply_text(text='Invalid command or message! Please try again.')
