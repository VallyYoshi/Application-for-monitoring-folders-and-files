import logging
import multiprocessing
import time

import keyboard
from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

event_handler = LoggingEventHandler()
observer = Observer()

counter = 1
answer = ''
folder_path = ''
folder_path_two = ''


def show_menu():
    print('Команды во время работы программы: \n'
          '1. Горячая клавиша "P" - Поставить программу на паузу\n'
          '2. Горячая клавиша "R" - Продолжить работу прогруммы\n'
          '3. Горячая клавиша "Q" - Выход из программы\n')


def start_work():

    global counter, folder_path, folder_path_two, answer

    while True:
        if counter == 1:
            folder_path = input('Введите путь к папке в которой хотите отслеживать изменения: ')
            answer = input('Хотите отслеживать изменение еще одной папки? (y/n): ')
        else:
            folder_path_two = input('Введите путь к папке в которой хотите отслеживать изменения: ')
            break

        if answer.lower() != 'y':
            break

        counter += 1

    if counter == 1:
        m = multiprocessing.Process(target=monitor_folder, args=(folder_path, 1,))
        m.start()
    else:
        m = multiprocessing.Process(target=monitor_folder, args=(folder_path, 1,))
        m_two = multiprocessing.Process(target=monitor_folder, args=(folder_path_two, 2,))
        m.start()
        m_two.start()


def monitor_folder(path, thread_number):

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    works = True

    try:
        while True:
            if keyboard.is_pressed('p') or keyboard.is_pressed('P'):
                if works:
                    observer.on_thread_stop()
                    works = False
                    print(f'Поток №{thread_number} приостановлен!')

            if keyboard.is_pressed('r') or keyboard.is_pressed('R'):
                if not works:
                    logging.basicConfig(level=logging.INFO,
                                        format='%(asctime)s - %(message)s',
                                        datefmt='%Y-%m-%d %H:%M:%S')

                    observer.schedule(event_handler, path, recursive=True)
                    observer.on_thread_start()

                    works = True

                    print(f'Поток №{thread_number} начал работу!')

            if keyboard.is_pressed('q') or keyboard.is_pressed('Q'):
                print(f'Поток №{thread_number} остоновлен!')
                observer.stop()
                break

            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    show_menu()
    start_work()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
