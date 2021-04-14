import pathlib
import sys


def parse_recursion(folder_path, file_names_dict, file_extentions_dict):

    # перебор всех объектов в папке и их анализ  
    for object in folder_path.iterdir():
        # если объект в папке - файл
        if object.is_file():

            if object.suffix.lower() in {'.jpeg', '.png', '.jpg', '.svg'}:
                file_names_dict[str(object.absolute())] = 'image'
                if file_extentions_dict.get(object.suffix.lower()) == None:
                    file_extentions_dict[object.suffix.lower()] = 'image'
                     
            elif object.suffix.lower() in {'.avi', '.mp4', '.mov', '.mkv'}:
                file_names_dict[str(object.absolute())] = 'video'
                if file_extentions_dict.get(object.suffix.lower()) == None:
                    file_extentions_dict[object.suffix.lower()] = 'video'

            elif object.suffix.lower() in {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'}:
                file_names_dict[str(object.absolute())] = 'docs'
                if file_extentions_dict.get(object.suffix.lower()) == None:
                    file_extentions_dict[object.suffix.lower()] = 'docs'        

            elif object.suffix.lower() in {'.mp3', '.ogg', '.wav', '.amr'}:
                file_names_dict[str(object.absolute())] = 'music'
                if file_extentions_dict.get(object.suffix.lower()) == None:
                    file_extentions_dict[object.suffix.lower()] = 'music'

            elif object.suffix.lower() in {'.zip', '.gz', '.tar'}:
                file_names_dict[str(object.absolute())] = 'archive'
                if file_extentions_dict.get(object.suffix.lower()) == None:
                    file_extentions_dict[object.suffix.lower()] = 'archive'

            else:
                file_names_dict[str(object.absolute())] = 'others'
                if file_extentions_dict.get(object.suffix.lower()) == None:
                    file_extentions_dict[object.suffix.lower()] = 'others'

        # если объект в папке - папка, вызываем рекурсию
        if object.is_dir():
            parse_recursion(object, file_names_dict, file_extentions_dict)

    return file_names_dict, file_extentions_dict        


def print_parsing_results(file_names_dict, file_extentions_dict):
    # вывод в консоль результатов работы
    print_dict = {'image': 'IMAGES',
                    'video': 'VIDEO',
                    'docs': 'DOCUMENTS',
                    'music': 'MUSIC',
                    'archive': 'ARCHIVE',
                    'others': 'OTHERS'
                    }

    for file_type_key, file_type_text in print_dict.items():
        flag = True 
        for key, value in file_names_dict.items():
            if value == file_type_key:
                if flag:
                    print(f'All {file_type_text} FILES:')
                print(key)
                flag = False

        flag = True
        for key, value in file_extentions_dict.items():
            if value == file_type_key:
                if flag:
                    print(f'All {file_type_text} EXTENTIONS:')
                print(key)
                flag = False


def parse_folder(folder_path):
    
    # проверка существует ли папка
    if folder_path.exists() == False:
        print(f'Указанная папка с путем {folder_path.absolute()} не существует')
        return
    if folder_path.exists() and (folder_path.is_dir() == False):
        print(f'Указанный путь {folder_path.absolute()} - не папка')
        return

    file_names_dict = dict()
    file_extentions_dict = dict()
    parse_recursion(folder_path, file_names_dict, file_extentions_dict)
    print_parsing_results(file_names_dict, file_extentions_dict)

    
def main():
    if len(sys.argv) == 1:
        print('Путь к папке не введен')
        return

    folder_path = sys.argv[1]
    folder_path = pathlib.Path(folder_path)
    parse_folder(folder_path)


if __name__ == '__main__':
    main()    