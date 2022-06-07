import os
import re
import shutil
import concurrent.futures


sort_folder = (input (f"Enter a path: "))


files = {"audio": ["mp3", "ogg", "wav", "amr"],
         "video": ["mp4", "avi", "mov", "mkv", "MOV"],
         "documents": ["doc", "docx", "txt", "pdf", "xlsx", "pptx", "rtf", "PDF", "xls"],
         "images": ["jpeg", "png", "jpg", "svg", "bmp", "BMP"],
         "archives": ["zip", "gz", "tar", "tgz", "rar"],
         "other": []}


def normalize(name):   # transliteration
    dictionary = {ord("А"): "A", ord("Б"): "B", ord("В"): "V", ord("Г"): "G", ord("Д"): "D", ord("Е"): "E", ord("Ж"): "ZH", ord("З"): "Z",
                  ord("И"): "I", ord("Й"): "J", ord("К"): "K", ord("Л"): "L", ord("М"): "M", ord("Н"): "N", ord("О"): "O", ord("П"): "P",
                  ord("Р"): "R", ord("С"): "S", ord("Т"): "T", ord("У"): "U", ord("Ф"): "F", ord("Х"): "H", ord("Ц"): "TS", ord("Ч"): "CH",
                  ord("Ш"): "SH", ord("Щ"): "SHCH", ord("Ь"): "", ord("Э"): "E", ord("Ю"): "YU", ord("Я"): "YA", ord("Ъ"): "", ord("Ы"): "Y",
                  ord("Ё"): "E", ord("Є"): "E", ord("І"): "Y", ord("Ї"): "YI", ord("Ґ"): "G",
                  ord("а"): "a", ord("б"): "b", ord("в"): "v", ord("г"): "g", ord("д"): "d", ord("е"): "e", ord("ж"): "zh", ord("з"): "z",
                  ord("и"): "y", ord("й"): "j", ord("к"): "k", ord("л"): "l", ord("м"): "m", ord("н"): "n", ord("о"): "o", ord("п"): "p",
                  ord("р"): "r", ord("с"): "s", ord("т"): "t", ord("у"): "y", ord("ф"): "f", ord("х"): "h", ord("ц"): "c", ord("ч"): "ch",
                  ord("ш"): "sh", ord("щ"): "shsc", ord("ь"): "", ord("э"): "e", ord("ю"): "yu", ord("я"): "ya", ord("ъ"): "", ord("ы"): "y",
                  ord("ё"): "e", ord("є"): "e", ord("і"): "y", ord("ї"): "yi", ord("ґ"): "g",
                  ord("1"): "1", ord("2"): "2", ord("3"): "3", ord("4"): "4", ord("5"): "5", ord("6"): "6", ord("7"): "7", ord("8"): "8", ord("9"): "9", ord("0"): "0"}
    en_name = name.translate(dictionary)
    fin_name = re.sub(r"(\W)", '_', en_name)
    return fin_name


dict_keys = list(dict.keys(files)) # Folder creates
for folder in dict_keys:
    os.chdir(sort_folder)
    folder = str(folder)
    if not os.path.isdir(folder):
        os.makedirs(folder)


def move(path):      # Move files in folders to destination
    el = ((path).split("\\"))
    sort_file = list(files.items())
    sufix = el[-1].split(".")[-1]
    file_name = "".join(el[-1].split(".")[0:-1])
    new_el = (normalize("".join(file_name)) + "." + sufix)
    el_moved = False
    for value in range(len(sort_file)):
        if sufix in sort_file[value][1]:
            os.rename(path, f'{sort_folder}\\{sort_file[value][0]}\\' + new_el)
            print(f'Moving {el} in {sort_file[value][0]} folder\n')
            el_moved = True
    if not el_moved:
        os.rename(path, f'{sort_folder}\\other\\' + new_el)
        print(f'Moving {el} in other folder\n')

def folder_sort(path):  # Рекурсивный проход по папкам
    path_len = len(" ".join(path).split("\\"))
    for folderName, subfolders, filenames in os.walk(path):
        try:
            folder = (folderName).split("\\")[path_len]    
        except:
            folder = None    
        if folder in dict_keys or folder == "other":
            pass
        else:
            files_list = []
            for el in filenames:
                files_list.append((f"{folderName}\\{el}"))
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                list(executor.map(move, files_list))


def remove_empty_dirs(path):  # Удаление пустых директорий
    for folderName, subfolders, filenames in os.walk(path):
        try:
            os.removedirs(folderName)
        except:
            pass


def unpackArchive (path):
    file_list = os.listdir(f'{path}\\archives')
    for el in file_list:
        sufix = el.split(".")[-1]
        file_name = el.split(".")[0:-1]
        if sufix in shutil.get_unpack_formats():
            shutil.unpack_archive (f'{path}\\archives\\{el}', f'{path}\\archives\\{file_name}\\{el}')


if __name__ == "__main__":


    folder_sort(sort_folder)
    unpackArchive(sort_folder)
    remove_empty_dirs(sort_folder)

#C:\Users\assa\Desktop\test

"""Доброго дня.
1. Коментарі мають бути англійською.                   done
2. Змінні не можуть називатись одним символом.         done
3. Спростіть вашу функцію move.                        done
Якщо ви робити в if break, 
и немає смислу далі писати else.
Удачі!"""