import os


class Path:
    def __init__(self, file_list):
        self.file_list = file_list
        self.file_dict = {}

    def search_paths(self):
        for path, subdirs, files in os.walk(os.getcwd(), topdown=False):
            for name in files:
                if name in self.file_list:
                    tpath = os.path.join(os.getcwd(), path)
                    spath = os.path.join(tpath, name)
                    self.file_dict[name] = spath

