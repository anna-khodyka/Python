import pickle
from datetime import datetime, timedelta
from collections import UserDict


class Field:
    value = None


class Name(Field):
    # хранит имя контакта в формате стринг
    def __init__(self, name):
        self.__value = None
        self.value = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Phone(Field):
    # хранит телефон в формате str
    def __init__(self, phone):
        self.__value = None
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        validated_tel = ''
        for i in new_value:
            if i in '0123456789':
                validated_tel += i
        if len(validated_tel) >= 10:
            self.__value = validated_tel
        else:
            raise TypeError('Введите номер из не менее 10 цифр')


class Birthday():  # не уверенна надо ли наследование от Field
    # хранит дату ДР в формате datetime
    def __init__(self):
        self.__value = None

    def __str__(self):
        if self.value == None:
            return ""
        else:
            return self.value.strftime('%d-%m-%Y')

    @property
    def value(self):
        return self.__value  # возвращает datetime

    @value.setter
    def value(self, new_value):  # new_value - str в формате '%d-%m-%Y' dd-mm-yyyy
        try:
            new_value = datetime.strptime(
                new_value, '%d-%m-%Y')
        except ValueError:
            raise TypeError(
                'Введенная дата не соответствует формату dd-mm-yyyy')
        if datetime(year=1900, month=1, day=1) < new_value < datetime.now():
            self.__value = new_value
        else:
            raise TypeError(
                f' Вы ввели нереальную дату рождения < 1900-01-01 или > {datetime.now().date()}')


class Record():

    def __init__(self, name, phone):
        self.name = Name(name)

        self.phones = list()
        if isinstance(phone, str):
            self.phones.append(Phone(phone))
        elif isinstance(phone, list):
            for ph in phone:
                self.phones.append(Phone(ph))

        self.birthday = Birthday()  # чему он должен равняться

    def __str__(self):
        result = f'{self.name.value} has a tel {self.get_phones()}'
        if str(self.birthday):
            result = result + " and has birthday " + str(self.birthday)
        return result

    def add_birthday(self, birthday_date):  # добавляет (записывает) ДР в запись
        self.birthday.value = birthday_date

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def days_to_birthday(self):
        # возвращает колво дней до ДР в int
        d = self.birthday.value.replace(year=datetime.now().year)
        if d - datetime.now() < timedelta(days=0):
            d = self.birthday.value.replace(year=1+datetime.now().year)
        return (d - datetime.now()).days

    def get_phones(self):
        phones_list = ''
        for phone in self.phones:
            phones_list += phone.value + ", "
        phones_list = phones_list.rstrip(', ')
        return phones_list


class AddressBook(UserDict):

    def add_birthday(self, name, birthday_str):
        self.data[name].add_birthday(birthday_str)

    def add_phone(self, name, phone):
        self.data[name].add_phone(phone)

    def add_record(self, name, phones):
        record = Record(name, phones)
        self.data[record.name.value] = record

    def change_phone(self, name, phone):
        self.data[name].phones = list()
        self.data[name].add_phone(phone)

    def days_to_birthday(self, name):
        return self.data[name].days_to_birthday()

    def iterator(self, n):
        # за одну итерацию возвращает строку - представление для N записей
        i = 0
        result = ""
        for record in anya_book.values():
            result += str(record)+"\n"
            i += 1
            if i == n:
                result = result.rstrip("\n")
                yield result
                result = ""
                i = 0
        if result:
            result = result.rstrip("\n")
            yield result

    def get_phones(self, name):
        return self.data[name].get_phones()

    def load_bin(self):
        file_name = 'anya_book.bin'
        with open(file_name, "rb") as fh:
            self.data = pickle.load(fh)
        return f"The adress book has succesfully uploaded from {file_name}"

    def save_bin(self):
        file_name = 'anya_book.bin'
        with open(file_name, "wb") as fh:
            pickle.dump(self, fh)
        return f"The adress book has succesfully saved to {file_name}"

    def find(self, word):  # дописать если нет ничего
        flag = False
        for record in self.data.values():
            if (word in record.name.value) or (word in record.get_phones()):
                print(record)
                flag = True
        if flag:
            result = "Search is sucessfully finished"
        else:
            result = f"No {word} in adress book"
        return result
################################################################################


anya_book = AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except TypeError as error:
            result = error
        return result
    return inner


def parse_command_input(client_input):
    client_input = client_input.strip()
    input_list = client_input.split(' ')

    # если команда из 2х слов
    if (input_list[0].lower() == 'show' and input_list[1].lower() == 'all'):
        input_list[0] = 'show_all'
        input_list.pop(1)
    if (input_list[0].lower() == 'good' and input_list[1].lower() == 'bye'):
        input_list[0] = 'good_bye'
        input_list.pop(1)

    command = input_list[0].lower()
    # если нет второго и третьего аргумента - технически заполняем их пустыми строками
    if len(input_list) > 1:
        name = input_list[1]
    else:
        name = ""
    if len(input_list) > 2:
        telephone = input_list[2]
    else:
        telephone = ""
    return command, name, telephone


@input_error
def do_hello(name, telephone):
    return "How can I help you?"


@input_error
def do_exit(name, telephone):
    return "Good bye!"


@input_error
def add(name, telephone):
    if not name:
        raise TypeError('Name is empty. Try again.')
    elif anya_book.get(name):
        anya_book.add_phone(name, telephone)
    elif not telephone:
        raise TypeError('Telephone is empty. Try again.')
    else:
        anya_book.add_record(name, telephone)
    return "I have saved " + anya_book.get_phones(name) + " as a telephone of "+name


@input_error
def change(name, telephone):
    if not telephone:
        raise TypeError('Telephone is empty. Try again.')
    elif not anya_book.get(name):
        raise TypeError('This name does not exist. Try again.')
    else:
        anya_book.change_phone(name, telephone)
    return "I have changed " + anya_book.get_phones(name) + " as a telephone of " + name


@input_error
def find(word, telephone):
    return anya_book.find(word)


@input_error
def print_by_pages(pages, telephone):
    pages = int(pages)
    if not anya_book:
        return "The contacts book is empty"
    else:
        print("The contacts book is following:")
        iter = anya_book.iterator(pages)
        for i in iter:
            print(i)
            print('========================================')
    return "The end of the contacts book"


@input_error
def save_bin(name, telephone):
    return anya_book.save_bin()


@input_error
def load_bin(name, telephone):
    return anya_book.load_bin()


@input_error
def show_all(name, telephone):
    return print_by_pages(len(anya_book), telephone)


@input_error
def add_birthday(name, bithday_str):
    if not name:
        raise TypeError('Name is empty. Try again.')
    elif not bithday_str:
        raise TypeError('Birthday is empty. Try again.')
    else:
        anya_book.add_birthday(name, bithday_str)
    return "I have saved " + anya_book.data[name].birthday + " as a birthday of "+name


@input_error
def days_to_birth(name, telephone):
    if not name:
        raise TypeError('Name is empty. Try again.')
    elif not anya_book.get(name):
        raise TypeError('This name does not exist. Try again.')
    else:
        return str(anya_book.days_to_birthday(name)) + " days till birthday of " + name


def handle_command(command):
    try:
        return COMMANDS[command]
    except KeyError:
        raise ValueError("Wrong direction! Try again.")


# словарь команда - функция что выполдняет команду
COMMANDS = {"hello": do_hello,
            "add": add,
            "find": find,
            "change": change,
            "show_all": show_all,
            "good_bye": do_exit,
            "exit": do_exit,
            "close": do_exit,
            "birthday": add_birthday,
            'days': days_to_birth,
            "print_by_pages": print_by_pages,
            "save": save_bin,
            "load": load_bin
            }


def main():

    print('''
Hello! My name is Hanna. I am your assistant    

I khow the following commands:
HELLO - to say hello
EXIT, CLOSE, GUD BUY - to exit from my programm

ADD - to add a new contact to adress book
CHANGE - to change phone in existed contact
FIND - to find name or phone or part of them

BIRTHDAY - to add birthday date in dd-mm-yyyy format
DAYS - to calculate the number of days to the next birthday

SHOW ALL - to show all the contacts in the adress book
PRINT_BY_PAGES - 
LOAD - to load the address book from file
SAVE - to save the address book to file
exit, close, bood buy - to exit from my programm
''')
    while True:
        client_input = input()

        # # парсинг клиенского ввода
        command, name, telephone = parse_command_input(client_input)

        try:
            result = handle_command(command)(name, telephone)
            print(result)
            if result == "Good bye!":
                break
        except ValueError as error:
            print(error)


if __name__ == '__main__':
    main()
