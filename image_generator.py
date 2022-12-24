from PIL import Image, ImageDraw

# Generate daily summary image
def generate_daily_summary_image(chat_id, completed_tasks, completed_habits, total_tasks, total_habits):
    # Calculate the percentage of tasks and habits completed
    task_percentage = (completed_tasks / total_tasks) * 100
    habit_percentage = (completed_habits / total_habits) * 100
    
    # Create the image
    image = Image.new('RGB', (400, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Draw the title
    draw.text((10, 10), 'Daily Summary', fill=(0, 0, 0))
    
    # Draw the completed tasks
    draw.text((10, 50), f'Completed Tasks: {completed_tasks}/{total_tasks} ({task_percentage:.2f}%)', fill=(0, 0, 0))
    
    # Draw the completed habits
    draw.text((10, 80), f'Completed Habits: {completed_habits}/{total_habits} ({habit_percentage:.2f}%)', fill=(0, 0, 0))
    
    # Save the image
    image.save(f'daily_summary_{chat_id}.png')

# Generate weekly summary image
def generate_weekly_summary_image(chat_id, completed_tasks, completed_habits, total_tasks, total_habits):
    # Calculate the percentage of tasks and habits completed
    task_percentage = (completed_tasks / total_tasks) * 100
    habit_percentage = (completed_habits / total_habits) * 100
    
    # Create the image
    image = Image.new('RGB', (400, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Draw the title
    draw.text((10, 10), 'Weekly Summary', fill=(0, 0, 0))
    
    # Draw the completed tasks
    draw.text((10, 50), f'Completed Tasks: {completed_tasks}/{total_tasks} ({task_percentage:.2f}%)', fill=(0, 0, 0))
    
    # Draw the completed habits
    draw.text((10, 80), f'Completed Habits: {completed_habits}/{total_habits} ({habit_percentage:.2f}%)', fill=(0, 0, 0))
    
    # Save the image
    image.save(f'weekly_summary_{chat_id}.png')
