import os
from config import Config
from sys import exit

ENCODING = 'utf-8'
CONFIG_FILE = 'config.ini'
OUTPUT_NAME_FILES = 'output_name_files.txt'
OUTPUT_COUNT_FILES = 'output_count_files.txt'


def scandir(path: str, level: int):
    count = 0
    try:
        with os.scandir(path) as scanDir:
            for entry in scanDir:
                if entry.is_dir(follow_symlinks=False):
                    sub_level = level - 1
                    dir_path, dir_count = scandir(entry.path, sub_level)
                    if level > 0:
                        print(f'{dir_path}, {dir_count}', file=open(OUTPUT_COUNT_FILES, mode='a', encoding=ENCODING))
                    count += dir_count
                elif entry.is_file(
                        follow_symlinks=False) and entry.name.endswith(config.extensionFile):
                    print(os.path.abspath(entry.path), file=open(OUTPUT_NAME_FILES, mode='a', encoding=ENCODING))
                    count += 1
        return path, count
    except Exception as exc:
        print(f"Directory '{path}' scan error: {exc}")
        return f'{path} - scan error', 0


def found_and_clear_output(output_name: str):
    if os.path.exists(output_name):
        print(f'File "{os.path.abspath(output_name)}" found and cleared.')
        try:
            os.remove(output_name)
        except Exception as exc:
            print(f"{exc}")
            input()
            exit()


if __name__ == '__main__':
    config = Config('config.ini')
    config.load()
    found_and_clear_output(OUTPUT_NAME_FILES)
    found_and_clear_output(OUTPUT_COUNT_FILES)
    if not os.path.exists(CONFIG_FILE):
        print(
            f'File "{CONFIG_FILE}" not found, modify the generated config file ("{os.path.abspath(CONFIG_FILE)}").'
        )
        result = config.save()
        print(result)
        input()
        exit()
    print('Started count files... ')
    path_dir, count_dir = scandir(config.pathFolder, config.levelDir)
    print(f'{path_dir}, {count_dir}', file=open(OUTPUT_COUNT_FILES, mode=ENCODING))
    print(f'Finished counting files ("{os.path.abspath(OUTPUT_COUNT_FILES)}"), press any button to exit.')
    input()
