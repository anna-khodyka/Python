tel_dict = dict()


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
    elif tel_dict.get(name):
        raise TypeError('This name already exists. Try again.')
    elif not telephone:
        raise TypeError('Telephone is empty. Try again.')
    else:
        tel_dict[name] = telephone
    return "I have saved "+telephone + " as a telephone of "+name


@ input_error
def change(name, telephone):
    if not telephone:
        raise TypeError('Telephone is empty. Try again.')
    elif not tel_dict.get(name):
        raise TypeError('This name does not exist. Try again.')
    else:
        tel_dict[name] = telephone
    return "I have changed "+telephone + " as a telephone of "+name


@ input_error
def find(name, telephone):
    if not name:
        raise TypeError('Name is empty. Try again.')
    elif not tel_dict.get(name):
        raise TypeError('This name does not exist. Try again.')
    else:
        return "The telephone of " + name + " is " + tel_dict[name]


@ input_error
def show_all(name, telephone):
    if not tel_dict:
        result = "The dictionary of telephones is empty"
    else:
        result = "The dictionary of telephones is following: \n"
        for key, value in tel_dict.items():
            result = result + key + " have a tel " + value + "\n"
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
