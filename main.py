import os
from config import Config
from sys import exit

CONFIG_FILE = 'config.ini'
OUTPUT_FILE = 'output.txt'


def scandir(path: str, level: int):
    count = 0
    try:
        with os.scandir(path) as scanDir:
            for entry in scanDir:
                if entry.is_dir(follow_symlinks=False):
                    sub_level = level - 1
                    dir_path, dir_count = scandir(entry.path, sub_level)
                    if level > 0:
                        print(f'{dir_path}, {dir_count}', file=open(OUTPUT_FILE, mode='a'))
                    count += dir_count
                elif entry.is_file(
                        follow_symlinks=False) and entry.name.endswith(config.extensionFile):
                    count += 1
        return path, count
    except Exception as exc:
        print(f"Directory '{path}' scan error: {exc}")
        return f'{path} - scan error', 0


if __name__ == '__main__':
    config = Config('config.ini')
    config.load()
    if os.path.exists(OUTPUT_FILE):
        print(f'File "{os.path.abspath(OUTPUT_FILE)}" found and cleared.')
        try:
            os.remove(OUTPUT_FILE)
        except Exception as exc:
            print(f"{exc}")
            input()
            exit()
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
    print(f'{path_dir}, {count_dir}', file=open(OUTPUT_FILE, mode='a'))
    print(f'Finished counting files ("{os.path.abspath(OUTPUT_FILE)}"), press any button to exit.')
    input()
