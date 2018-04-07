
from PyQt5.QtCore import QDir, QDirIterator


def countFiles(self, folder):
    files = []

    if self.subfolderLevel > 0:
        try:
            path = glob.glob('%s/%s' %
                                (folder, '*/'*self.subfolderLevel))[0]
            self.pathToDisplay = path
        except:
            return 0
    else:
        path = folder

    it = QDirIterator(
        path, (QDir.Files | QDir.NoSymLinks), self.countRecursivity)
    while it.hasNext():
        files.append(it.next())

    count = len(files)
    return count
