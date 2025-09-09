from datetime import datetime
from models import Task

#--- Menu ---
def show_menu():
    print(
        '--- To-Do List ---',
        '1. Show tasks',
        '2. Add a new task',
        '3. Update task',
        '4. Mark task as done', 
        '5. Delete a task',
        '6. Exit',
        sep='\n'
        )

def get_user_choice(range:str):
    return input(f'Choose an option ({range}): ')

#--- Show tasks ---
def select_filter()-> None:
    print(
        'Filters:',
        '1. All tasks',
        '2. Only active',
        '3. Only completed', 
        '4. By date',
        '5. By priority',
        sep='\n'
        )
    
def select_field_for_update() -> None:
    print(
        'Task:',
        '1. Update title',
        '2. Update description',
        '3. Update deadline', 
        '4. Update priority',
        '5. Cansel',
        sep='\n'
        )
    


def show_tasks(tasks:list[Task])->None:
    if tasks: 
        for i, task in enumerate(tasks, start=1):
            status = '✅' if task['done'] else '❌'
            print(f'{i}. {task['title']} - {status}')
    else:
        print('No tasks found.')

def show_task_datails(tasks:list[Task], ind) -> None:
    if ind == -1:
        return None
    elif tasks:
        task = tasks[ind]
        print(f'Title: {task.title}',
              f'Status: {'✅' if task.done else '❌'}',
              f'Description: {task.description}',
              f'Deadline: {task.deadline}',
              f'Priority: {task.priority}', 
              f'Date of creation: {task.created_at}',
              f'Вate of completion: {task.completed_at}',
              sep='\n'
              )
    else:
        return None



def get_task_title():
    while True: 
        title = input('Enter task title: ')
        if title == '':
            print('You cannot enter a blank task name. Please try again.')
        else: 
            return title

def get_task_description():
    description = input('Enter task description (optional): ')
    if description == '':
        return None
    return description 

def get_task_deadline():
    while True: 
        deadline_str = input('Enter task deadline (YYYY-MM-DD HH:MM) or leave blank: ')
        if deadline_str == '':
            return None
        try:
            return datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
        except ValueError:
            print('Invalid date format. Please use YYYY-MM-DD HH:MM.')

def get_date_period():
    while True:
        date_from = input('Enter date from (YYYY-MM-DD HH:MM): ')
        date_to = input('Enter date to(YYYY-MM-DD HH:MM): ')
        if date_from == '' or date_to =='':
            print('Invalid date format. Please use YYYY-MM-DD HH:MM.')
        try:
            return {'date_from': datetime.strptime(date_from, '%Y-%m-%d %H:%M'), 'date_to': datetime.strptime(date_to, '%Y-%m-%d %H:%M')}
        except ValueError:
            print('Invalid date format. Please use YYYY-MM-DD HH:MM.')
                    

def get_task_priority():
    while True:
        value = input('Enter task priority 0-5 (default 0): ').strip()
        if value == '':
            return 0
        try:
            priority = int(value)
            if 0 <= priority <= 5:
                return priority
            else:
                print('Invalid number entered. Please, enter digit from 0 to 5.')
        except ValueError: 
            print('Invalid value entered. Please, enter digit from 0 to 5.')
    

    
def get_task_ind():
    try:
        return int(input('Enter task number: '))
    except ValueError:
        print('Invalid input. Please enter a number.')
        return None

def show_message(message):
    print(message)


