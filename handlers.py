from sqlalchemy.orm import Session

import db_functions as db_f
import ui


def handle_show_tasks(db: Session) -> None:
    ui.select_filter()
    choice_f = ui.get_user_choice("1-6")
    if choice_f == "1":
        tasks = db_f.get_all_tasks(db)
        ui.show_tasks([task.__dict__ for task in tasks])
        ui.show_message('Enter the task index for detailed view or press "0" to cancel')
    elif choice_f == "2":
        tasks = db_f.get_tasks_by_status(db, False)
        ui.show_tasks([task.__dict__ for task in tasks])
    elif choice_f == "3":
        tasks = db_f.get_tasks_by_status(db, True)
        ui.show_tasks([task.__dict__ for task in tasks])
    elif choice_f == "4":
        period = ui.get_date_period()
        tasks = db_f.get_tasks_by_deadline(db, period["date_from"], period["date_to"])
        ui.show_tasks([task.__dict__ for task in tasks])
    elif choice_f == "5":
        tasks = db_f.get_tasks_by_priority(db, ui.get_task_priority())
        ui.show_tasks([task.__dict__ for task in tasks])
    
    choice_task = ui.get_task_ind()-1
    ui.show_task_datails(tasks, choice_task)


def handle_add_tasks(db: Session):
    task = db_f.create_task(
        db,
        title=ui.get_task_title(),
        description=ui.get_task_description(),
        deadline=ui.get_task_deadline(),
        priority=ui.get_task_priority(),
    )
    ui.show_message(f'Task "{task.title}" is created.')

def handle_update_task(db: Session) -> None:
    tasks = db_f.get_all_tasks(db)
    ui.show_tasks([task.__dict__ for task in tasks])
    ind = ui.get_task_ind()-1
    if 0 <= ind <= len(tasks):
        task = tasks[ind]
        if task:
            ui.select_field_for_update()
            choice_up = ui.get_user_choice('1-5')
            if choice_up == '1':
                new_title = ui.get_task_title()
                new_task = db_f.update_task(db, task.id, new_title=new_title)
                ui.show_message(f'The task "{task.title}" -> "{new_task.title}" has been updated.')
            elif choice_up == '2':
                new_description = ui.get_task_description()
                new_task = db_f.update_task(db, task.id, new_description=new_description)
                ui.show_message(f'The task "{new_task.title}" has been updated.')
            elif choice_up == '3':
                new_deadline = ui.get_task_deadline()
                new_task = db_f.update_task(db, task.id, new_deadline=new_deadline)
                ui.show_message(f'The task "{new_task.title}" has been updated.')
            elif choice_up == '4':
                new_priority = ui.get_task_priority()
                new_task = db_f.update_task(db, task.id, new_priority=new_priority)
                ui.show_message(f'The task "{new_task.title}" has been updated.')
            elif choice_up == '5':
                ui.show_message(f'Task update cancelled')
            elif choice_up == '':
                ui.show_message(f'Task update cancelled')


def handle_mark_task_as_done(db: Session) -> None:
    tasks = db_f.get_all_tasks(db)
    ui.show_tasks([task.__dict__ for task in tasks])
    ind = ui.get_task_ind() - 1
    if 0 <= ind < len(tasks):
        task = tasks[ind]
        if task:
            task = db_f.mark_task_as_done(db, task.id)
            ui.show_message(f'Task "{task.title}" is accomplished.')
        else:
            ui.show_message("Task not found.")
    else:
        ui.show_message("Invalid task number")


def handle_delete_task(db: Session) -> None:
    tasks = db_f.get_all_tasks(db)
    ui.show_tasks([task.__dict__ for task in tasks])
    ind = ui.get_task_ind() - 1
    if 0 <= ind < len(tasks):
        task = tasks[ind]
        if task:
            task = db_f.delete_task(db, task.id)
            ui.show_message(f'Task "{task.title}" is deleted.')
        else:
            ui.show_message("Task not found.")
    else:
        ui.show_message("Invalid task number")
