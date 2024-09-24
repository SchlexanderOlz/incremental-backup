import backup

def create():
    old = backup.Backup.load_from_file("20240924200928")
    backup.Backup("saus", old.tree).dump()

def restore():
    restore = backup.Restorer(["20240924200928", "20240924201033"])
    restore.restore("out")

   

if __name__ == "__main__":
    restore()


