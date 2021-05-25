from collections import UserDict


class Field():
    value = None


class Name(Field):
    # хранит имя контакта в формате стринг
    def __init__(self, name):
        self.value = name


class Phone(Field):
    # хранит телефон в формате стринг
    def __init__(self, phone):
        self.value = phone


class Record():

    def __init__(self, name, phone):
        self.name = Name(name)

        self.phones = list()
        if isinstance(phone, str):
            self.phones.append(Phone(phone))
        elif isinstance(phone, list):
            for ph in phone:
                self.phones.append(Phone(ph))

    def get_phones(self):
        phones_list = ''
        for phone in self.phones:
            phones_list += phone.value + " "
        return phones_list

    def add_phone(self, phone):
        self.phones.append(Phone(phone))


class AddressBook(UserDict):
    # добавляет Record в self.data

    def add_record(self, name, phones):
        record = Record(name, phones)
        self.data[record.name.value] = record

    def get_phones(self, name):
        return self.data[name].get_phones()

    def add_phone(self, name, phone):
        self.data[name].add_phone(phone)

    def change_phone(self, name, phone):
        self.data[name].phones = list()
        self.data[name].add_phone(phone)

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


@ input_error
def do_hello(name, telephone):
    return "How can I help you?"


@ input_error
def do_exit(name, telephone):
    return "Good bye!"


@ input_error
def add(name, telephone):
    if not name:
        raise TypeError('Name is empty. Try again.')
    elif anya_book.get(name):
        anya_book.add_phone(name, telephone)
    elif not telephone:
        raise TypeError('Telephone is empty. Try again.')
    else:
        anya_book.add_record(name, telephone)
    return "I have saved " + anya_book.get_phones(name) + "as a telephone of "+name


@ input_error
def change(name, telephone):
    if not telephone:
        raise TypeError('Telephone is empty. Try again.')
    elif not anya_book.get(name):
        raise TypeError('This name does not exist. Try again.')
    else:
        anya_book.change_phone(name, telephone)
    return "I have changed " + anya_book.get_phones(name) + "as a telephone of " + name


@ input_error
def find(name, telephone):
    if not name:
        raise TypeError('Name is empty. Try again.')
    elif not anya_book.get(name):
        raise TypeError('This name does not exist. Try again.')
    else:
        return "The telephone of " + name + " is " + anya_book.get_phones(name)


@ input_error
def show_all(name, telephone):
    if not anya_book:
        result = "The dictionary of telephones is empty"
    else:
        result = "The dictionary of telephones is following: \n"
        for key, record in anya_book.items():
            result = result + key + " have a tel " + \
                record.get_phones() + "\n"
        result = result.rstrip("\n")
    return result


def handle_command(command):
    try:
        return COMMANDS[command]
    except KeyError:
        raise ValueError("Wrong direction! Try again.")


# словарь команда - функция что выполдняет команду
COMMANDS = {"hello": do_hello, "add": add, "find": find, "change": change, "show_all": show_all, "good_bye": do_exit,
            "exit": do_exit, "close": do_exit}


def main():

    print('Hello! My name is Hanna. I am your assistant')
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
