import backup

def create():
    """
    Creates a new backup by comparing the current state of the "saus" directory
    with an existing backup from a file named "20240925122027". The differences
    are identified, and the new backup is saved.

    Steps:
    1. Loads an existing backup from the file "20240925122027".
    2. Compares the state of the "saus" directory with the previously loaded backup.
    3. Creates a new backup that stores the changes (if any).
    4. Saves the new backup with a timestamped filename.
    """
    old = backup.Backup.load_from_file("20240925122027")  # Load previous backup
    created = backup.Backup("saus", old=old.tree).dump()  # Create and save the new backup

def create_initial():
    """
    Creates an initial backup for the "saus" directory without comparing it to any 
    previous backup. This is useful for starting a new backup process for the directory.

    Steps:
    1. Scans the "saus" directory and creates a full backup.
    2. Saves the initial backup with a timestamped filename.
    """
    created = backup.Backup("saus").dump()  # Create and save the initial backup

def restore():
    """
    Restores the "saus" directory to the state captured in a series of backups. It
    uses two backups, "20240925122027" and "20240925122131", and applies them in order
    to ensure that the destination reflects the latest changes.

    Steps:
    1. Loads two backup files ("20240925122027" and "20240925122131").
    2. Restores the files to the "out" directory in chronological order.
    """
    restore = backup.Restorer(["20240925122027", "20240925122131"])  # Load multiple backups
    restore.restore("out")  # Apply the changes to the "out" directory

if __name__ == "__main__":
    # If the script is run directly, it will trigger the restore process
    restore()
