import logging

from models import models_main, session

import db_functions as db_f
import ui
from handlers import (
    handle_show_tasks,
    handle_add_tasks,
    handle_update_task,
    handle_mark_task_as_done,
    handle_delete_task
)

#--- Logging cofiguration ---
logger = logging.getLogger(__name__)
logging.basicConfig(
   level=logging.INFO,
   format='%(filename)s:%(lineno)d #%(levelname)-8s '
          '[%(asctime)s] - %(name)s - %(message)s'
          )

#--- Main Function ---
def main():
    logger.info('Starting application')

    # Create database and tables
    models_main()
    logger.info('Database and tables created')

    # Create a new database session
    db = session()
    logger.info('Database session created')
    
    try:
    #--- Main loop ---
        while True:
            ui.show_menu()
            choice = ui.get_user_choice('1-5')
            
            # Show tasks
            if choice == '1':
                handle_show_tasks(db)

            # Add a new task
            elif choice == '2':
                handle_add_tasks(db)             
            
            # Update task
            elif choice == '3':
                handle_update_task(db)
                
            # Mark task as done
            elif choice == '4':
                handle_mark_task_as_done(db)

            
            # Delete a task        
            elif choice == '5':
               handle_delete_task(db)           

            # Exit
            elif choice == '6':
                ui.show_message('Goodbye!')
                break

            elif choice == '':
                continue

            else:
                ui.show_message('Invalid option. Please try again.')
    
    finally:
        db.close()
        logger.info('Database session closed')
            
if __name__ == '__main__':
   main()



