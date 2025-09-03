
tasks = []

def show_tasks(tasks):
    if tasks:
      for i, task in enumerate(tasks, start=1):
         status = '✅' if task['done'] else '❌'
         print(f'{i}. {task['title']} {status}')
    else:
      print('Няма задачаў')

def add_task(tasks, title):
    tasks.append({'title': title, 'done': False})
    print(f'Задача "{title}" паспяхова дададзена!')

def complete_task(tasks, index):
    if 0 <= index <= len(tasks):
      tasks[index]['done'] = True
      print(f'Задача "{tasks[index]['title']}" выканана!')
    else: 
       print('Няправильны нумар')

def delete_task(tasks, index):
   if 0 <= index <= len(tasks):
        removed = tasks.pop(index)
        print(f'Задача "{removed['title']}" выдалена са спісу')
   


def main():
   print('--- To-Do List ---',
         '1. Паказаць усе задачы',
         '2. Дадаць задачу',
         '3. Выканаць задачу',
         '4. Выдаліць задачу',
         '5. Выйсці',
         sep='\n')
   

   while True:
    choice = input('Абярыце опцыю: ')
    if choice == '1':
        show_tasks(tasks)
    elif choice == '2':
       title = input('Увядзіце задачу: ')
       add_task(tasks, title)
    elif choice == '3':
        try:
            index = int(input('Увядзіце нумар задачы: '))-1
            complete_task(tasks, index)
        except:
            print('Вы ўвялі няправільную лічбу')
          
    elif choice == '4':
        try:
            index = int(input('Увядзіце нумар задачы: '))-1
            delete_task(tasks, index)
        except:
            print('Вы ўвялі няправільную лічбу')
    elif choice == '5':
       print('Да пабачэння!')
       break
    else: 
       print('Няправільны выбар')


if __name__ == '__main__':
   main()
