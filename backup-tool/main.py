import backup

def create():
    old = backup.Backup.load_from_file("20240925122027")
    created = backup.Backup("saus", old=old.tree).dump()

def create_initial():
    created = backup.Backup("saus").dump()


def restore():
    restore = backup.Restorer(["20240925122027", "20240925122131"])
    restore.restore("out")



if __name__ == "__main__":
    restore()