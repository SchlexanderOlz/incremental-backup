import backup

def create():
    old = backup.Backup.load_from_file("20240925103228")
    old2 = backup.Backup.load_from_file("20240925103330", old=old.tree)

    created = backup.Backup("saus", old=old2.tree).dump()

def create_initial():
    created = backup.Backup("saus").dump()


def restore():
    restore = backup.Restorer(["20240925103228", "20240925103330", "20240925113036"])
    restore.restore("out")



if __name__ == "__main__":
    create()
    print("")
    print("")
    print("CREATED BACKUP")
    print("")
    print("")
    restore()
