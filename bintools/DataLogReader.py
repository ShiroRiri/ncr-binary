import struct

from crccheck.crc import Crc32
from .FieldTypes import FieldTypes

class DataLogReader:
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.__readHeader()
        
    def __readHeader(self):
        magic = bytes('NC🚀2019', 'utf-8')
        fileMagic = self.file.read(len(magic))
        
        if (magic != fileMagic):
            raise Exception('File magic invalid. File may be corrupted :()')
            
        fieldsLength = struct.unpack('H', self.file.read(2))[0]
        self.fields = []
        
        for i in range(0, fieldsLength):
            meta = struct.unpack('HBB', self.file.read(4))
            
            fieldId = meta[0]
            nameLength = meta[2]
            type = FieldTypes(meta[1])
            
            if (fieldId != i):
                raise Exception('Field ordering invalid. File may be corrupted :()')
                
            name = self.file.read(nameLength).decode('utf8')
            
            self.fields.append({'name': name, 'type': type})
