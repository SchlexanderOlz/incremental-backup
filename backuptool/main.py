import backup
from sys import argv
from os import listdir

def create(dir: str, prev_backup: str):
    """
    Creates a new incremental backup by comparing the current state of the directory
    with a previous backup.
    
    Args:
        dir (str): The directory to back up.
        prev_backup (str): The file containing the previous backup to compare against.

    Steps:
    1. Loads the previous backup from the specified file.
    2. Compares the current state of the directory with the old backup.
    3. Creates and saves a new backup file with a timestamped filename.
    """
    old = backup.Backup.load_from_file(prev_backup)  # Load previous backup
    created = backup.Backup(dir, old=old.tree).dump()  # Create and save the new backup

def create_initial(dir: str):
    """
    Creates an initial backup of a directory without comparing it to any previous backup.
    
    Args:
        dir (str): The directory to back up.

    Steps:
    1. Scans the directory for all files and directories.
    2. Creates and saves the initial backup with a timestamped filename.
    """
    created = backup.Backup(dir).dump()  # Create and save the initial backup

def restore(backup_files: list[str]):
    """
    Restores the state of the directory using a list of backup files.
    
    Args:
        backup_files (list[str]): List of backup filenames to restore from.
    
    Steps:
    1. Loads the provided backup files in chronological order.
    2. Applies each backup to restore the directory's state to the latest version.
    """
    restore = backup.Restorer(backup_files)  # Load backup files
    restore.restore("out")  # Restore to the 'out' directory

if __name__ == "__main__":
    """
    Command-line interface for creating and restoring backups.
    - Use '--create' to create an incremental backup.
    - Use '--create-initial' to create an initial backup.
    - Use '--restore' to restore from a series of backup files.

    Expected usage:
    1. --create <directory> <previous_backup_file>
    2. --create-initial <directory>
    3. --restore <backup_file1> <backup_file2> ...
    """
    if len(argv) < 2:
        print("Invalid argument")  # Print error if no arguments are provided
        exit(1)

    # Create an incremental backup
    if argv[1] == "--create":
        if len(argv) != 4:
            print("Invalid argument")  # Ensure the correct number of arguments
            exit(1)
        dirname = argv[2]  # Directory to back up
        filename = argv[3]  # Previous backup file
        create(dirname, filename)

    # Create an initial backup
    elif argv[1] == "--create-initial":
        if len(argv) != 3:
            print("Invalid argument")  # Ensure the correct number of arguments
            exit(1)
        dir = argv[2]  # Directory to back up
        create_initial(dir)

    # Restore from a set of backup files
    elif argv[1] == "--restore":
        if len(argv) < 3:
            print("Invalid argument")  # Ensure there are backup files to restore from
            exit(1)
        files = argv[2:]  # Get the list of backup files provided by the user
        
        # Expand wildcard '*' in filenames to match multiple files
        for file in files:
            if file.endswith("*"):  # Handle wildcard ending
                files.remove(file)
                files.extend([file for file in listdir(".") if file.startswith(file[:-1])])
        
        restore(files)  # Perform the restore operation

    # Handle invalid command-line options
    else:
        print("Invalid argument")
