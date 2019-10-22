class DataLogReader:
    def __init__(self, filename):
        self.file = open(filename, 'rb')
