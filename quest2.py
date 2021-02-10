import os
import time
import shutil
from termcolor import cprint, colored


_help = False


def main():
    os.system('clear')
    header()
    db = loadPass()
    flagAuth = False
    while True:
        inp = input()
        x = inp.split()
        os.system('clear')
        header()
        print(inp, '\n')
        if x[0] == 'help':
            help_m()
        elif x[0] == 'auth':
            flagAuth = auth_m(db, x)
        elif x[0] == 'exit':
            cprint('До скорых встреч!\n', 'yellow')
            break
        elif checkAuth(flagAuth):
            if x[0] == 'list':
                list_m()
            elif x[0] == 'info':
                info_m(x)
            elif x[0] == 'retr':
                retr_m(x)
            else:
                cprint('Ошибка: Неизвестная команда\n', 'red')


def header():
    cprint('\nДоброго времени суток!', 'white')
    cprint('Добро пожаловать на VladoServer', 'blue')
    cprint('Введите help - для получения справки\n', 'red')


def checkAuth(flag):
    if flag:
        return True
    else:
        if _help:
            help_m()
        cprint('Ошибка: Сначала авторизуйтесь\n', 'red')
        return False


def help_m():
    global _help
    _help = True
    cprint('auth user pass - авторизоваться, user - логин, pass - пароль', 'yellow')
    cprint('list — показать список файлов в каталоге запуска программы', 'yellow')
    cprint('info file — напечатать сведения о файле, тип, размер, время создания', 'yellow')
    cprint('retr file1 file2 file_n — передать файлы, указанные в строке.', 'yellow')
    cprint('exit — выход\n', 'yellow')


def retr_m(x):
    if _help:
        help_m()
    if len(x) == 1:
        cprint('Ошибка: Введите файл(ы)\n', 'red')
        return
    for i in range(1, len(x)):
        shutil.copy(x[i], '/mnt/d/Времяночка/Vlad/ВУЗ/2 курс/2 трим/АИС/Лаб 2/Лаба 2/CopyFolder')
        print(colored(x[i], 'white'), colored('скопирован', 'white'))
    cprint('Копирование закончено\n', 'blue')


def info_m(x):
    if _help:
        help_m()
    if len(x) == 1:
        cprint('Ошибка: Введите файл\n', 'red')
        return
    if os.path.exists(x[1]):
        print(colored('файл:', 'white'), colored(x[1], 'white'))
        print(colored('тип:', 'white'), colored(x[1].split('.')[1], 'white'))
        print(colored('размер:', 'white'), colored(os.path.getsize(x[1]), 'white'), colored('bytes', 'white'))
        print(colored('дата создания:', 'white'), colored(time.ctime(os.path.getctime(x[1])), 'white'))
        print()
    else:
        cprint('Ошибка: Файл не существует!\n', 'red')


def list_m():
    if _help:
        help_m()
    for file in os.listdir('.'):
        if os.path.isfile(os.path.join('.', file)):
            print(file)
    print()


def auth_m(db, x):
    global _help
    if _help:
        help_m()
    if len(x) < 3:
        cprint('Ошибка: Введите логин и пароль\n', 'red')
        return
    flagAuth = False
    for user in db:
        if user == x[1]:
            if db.get(user) == x[2]:
                cprint('Авторизация прошла успешно\n', 'blue')
                flagAuth = True
                break
    else:
        cprint('Ошибка: Неверный логин или пароль\n', 'red')
    return flagAuth


def loadPass():
    db = {}
    with open("pass.txt") as file:
        for line in file:
            key, value = line.split()
            db[key] = value
    return db


main()
