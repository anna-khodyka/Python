from datetime import datetime, timedelta
from collections import defaultdict


def congratulate(users):
    current_datetime = datetime.now()

    # определение начала и конца следующей недели
    if current_datetime.weekday() != 6:
        saturday = current_datetime.date() + \
            timedelta(days=(5-current_datetime.weekday()))
    else:
        saturday = current_datetime.date() - timedelta(days=1)

    friday = current_datetime.date() + \
        timedelta(days=7+(4-current_datetime.weekday()))

    # поиск в списке users именинников и запись их в словарь списков словарей (ключ - день недели, список именн)
    bith_list = defaultdict(list)
    for user in users:
        user['birthday'] = user['birthday'].replace(current_datetime.year)

        if saturday <= user['birthday'].date() <= friday:
            key = user['birthday'].strftime('%A')
            if key == 'Saturday' or key == 'Sunday':
                key = 'Monday'
            bith_list[key].append(user)

    # сортировка словаря по дням недели
    sorted_bith_list = dict()
    WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
    for day in WEEKDAYS:
        if bith_list[day]:
            sorted_bith_list[day] = bith_list[day]

    # Печать списка именинников
    if not sorted_bith_list:
        s = saturday.strftime('%d:%m:%Y')
        f = friday.strftime('%d:%m:%Y')
        print(f'Нет именинников на следующей недели с {s} по {f}')
    else:
        for key, value in sorted_bith_list.items():
            result = key+': '
            for person in value:
                result += person['name']+', '
            result = result.rstrip().removesuffix(',')+'\n'
            print(result)


def main():
    users = [{'name': 'Hanna', 'birthday': datetime.strptime('21-05-1993', '%d-%m-%Y')},
             {'name': 'Denis', 'birthday': datetime.strptime(
                 '14-05-1985', '%d-%m-%Y')},
             {'name': 'Olga', 'birthday': datetime.strptime(
                 '17-05-2000', '%d-%m-%Y')},
             {'name': 'Borya', 'birthday': datetime.strptime(
                 '22-05-1974', '%d-%m-%Y')},
             {'name': 'Alexandr', 'birthday': datetime.strptime(
                 '20-05-1995', '%d-%m-%Y')},
             {'name': 'Tetyana', 'birthday': datetime.strptime(
                 '15-05-1984', '%d-%m-%Y')},
             ]

    congratulate(users)


if __name__ == '__main__':
    main()
