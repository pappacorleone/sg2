import telegram

# Function to check if the user is in the process of adding a task
def is_adding_task(user_id):
    # Check if the adding task flag is set in the user's session data
    return 'adding_task' in context.user_data and context.user_data['adding_task']

# Function to set the adding task flag in the user's session data
def set_adding_task(user_id):
    context.user_data['adding_task'] = True

# Function to clear the adding task flag in the user's session data
def clear_adding_task(user_id):
    if 'adding_task' in context.user_data:
        del context.user_data['adding_task']

# Function to check if the user is in the process of adding a habit
def is_adding_habit(user_id):
    # Check if the adding habit flag is set in the user's session data
    return 'adding_habit' in context.user_data and context.user_data['adding_habit']

# Function to set the adding habit flag in the user's session data
def set_adding_habit(user_id):
    context.user_data['adding_habit'] = True

# Function to clear the adding habit flag in the user's session data
def clear_adding_habit(user_id):
    if 'adding_habit' in context.user_data:
        del context.user_data['adding_habit']

# Function to check if the user is in the process of updating a task or habit
def is_updating(user_id):
    # Check if the updating flag is set in the user's session data
    return ' ------------------------------ 
# Function to check if the user is in the process of deleting a task or habit
def is_deleting(user_id):
    # Check if the deleting flag is set in the user's session data
    return 'deleting' in context.user_data and context.user_data['deleting']

# Function to set the deleting flag in the user's session data
def set_deleting(user_id):
    context.user_data['deleting'] = True

# Function to clear the deleting flag in the user's session data
def clear_deleting(user_id):
    if 'deleting' in context.user_data:
        del context.user_data['deleting']

# Function to check if the user is in the process of selecting the status of a task or habit
def is_selecting_status(user_id):
    # Check if the selecting status flag is set in the user's session data
    return 'selecting_status' in context.user_data and context.user_data['selecting_status']

# Function to set the selecting status flag in the user's session data
def set_selecting_status(user_id):
    context.user_data['selecting_status'] = True

# Function to clear the selecting status flag in the user's session data
def clear_selecting_status(user_id):
    if 'selecting_status' in context.user_data:
        del context.user_data['selecting_status']

# Function to generate an infographic summary image of the user's progress for the day
def generate_daily_summary_image(tasks, habits):
    # Create the image
    image = Image.new('RGB', (800, 600), color=(73, 109, 137))
    draw = ImageDraw.Draw(image)
    
    # Add the title text
    draw.text((10, 10), 'Daily Progress Summary', fill=(255, 255, 255))
    
    # Add the tasks and habits to the image
    y = 50
    for task in tasks: ------------------------------
        # Add the task or habit text to the image
    draw.text((10, y), '{}: {}'.format(task_or_habit_type, task_or_habit_name), fill=(255, 255, 255))
    
    # Increment the y-coordinate
    y += 30

# Function to generate an infographic summary image of the user's progress for the week
def generate_weekly_summary_image(tasks, habits):
    # Create the image
    image = Image.new('RGB', (800, 600), color=(73, 109, 137))
    draw = ImageDraw.Draw(image)
    
    # Add the title text
    draw.text((10, 10), 'Weekly Progress Summary', fill=(255, 255, 255))
    
    # Add the tasks and habits to the image
    y = 50
    for task in tasks:
        # Check if the task was completed
        if task[3] == 1:
            completed = 'Completed'
        else:
            completed = 'Incomplete'
        
        # Add the task text to the image
        draw.text((10, y), 'Task: {} ({})'.format(task[2], completed), fill=(255, 255, 255))
        
        # Increment the y-coordinate
        y += 30
        
    for habit in habits:
        # Check if the habit was completed
        if habit[4] == 1:
            completed = 'Completed'
        else:
            completed = 'Incomplete'
        
        # Add the habit text to the image
        draw.text((10, y), 'Habit: {} ({})'.format(habit[2], completed), fill=(255, 255, 255))
        
        # Increment the y-coordinate
        y += 30
    
    return image

