import backup

def create():
    old = backup.Backup.load_from_file("20240924195940")
    backup.Backup("saus", old.tree).dump()

def restore():
    restore = backup.Restorer(["20240924195940", "20240924200352"])
    restore.restore("out")

   

if __name__ == "__main__":
    restore()


