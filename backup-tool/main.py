import backup

def create():
    old = backup.Backup.load_from_file("20240924213437")

    created = backup.Backup("saus", old=old.tree).dump()



def restore():
    restore = backup.Restorer(["20240924213437", "20240924213533"])
    restore.restore("out")

   

if __name__ == "__main__":
    restore()


