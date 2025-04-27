import os

script_dir = os.path.dirname(__file__)

PATH_FILE = os.path.join(script_dir, "./data/operations.xlxs")

if not os.path.exists(PATH_FILE):
    print(f"Ошибка: файл {PATH_FILE} не найден!")
