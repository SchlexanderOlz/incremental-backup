import backup
from sys import argv
from os import listdir

def create(dir: str, prev_backup: str):
    old = backup.Backup.load_from_file(prev_backup)
    created = backup.Backup("saus", old=old.tree).dump()

def create_initial(dir: str):
    created = backup.Backup(dir).dump()


def restore(backup_files: list[str]):
    restore = backup.Restorer(backup_files)
    restore.restore("out")



if __name__ == "__main__":
    if len(argv) < 2:
        print("Invalid argument")
        exit(1)
    if argv[1] == "--create":
        if len(argv) != 4:
            print("Invalid argument")
            exit(1)
        dirname = argv[2]
        filename = argv[3]
        create(dirname, filename)
    elif argv[1] == "--create-initial":
        if len(argv) != 3:
            print("Invalid argument")
            exit(1)
        dir = argv[2]
        create_initial(dir)
    elif argv[1] == "--restore":
        if len(argv) < 3:
            print("Invalid argument")
            exit(1)
        files = argv[2:]
        for file in files:
            if file.endswith("*"):
                files.remove(file)
                files.extend([file for file in listdir(".") if file.startswith(file[:-1])])
        restore(files)
    else:
        print("Invalid argument")
