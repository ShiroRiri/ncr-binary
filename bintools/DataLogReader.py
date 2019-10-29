import struct

from crccheck.crc import Crc32
from .FieldTypes import FieldTypes

class DataLogReader:
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.sampleCounter = 0
        self.__readHeader()

    def __readHeader(self):
        magic = bytes('NC🚀2019', 'utf-8')
        fileMagic = self.file.read(len(magic))

        if (magic != fileMagic):
            raise Exception('File magic invalid. File may be corrupted :(')

        fieldsLength = struct.unpack('<H', self.file.read(2))[0]
        self.fields = []

        for i in range(0, fieldsLength):
            meta = struct.unpack('<HBB', self.file.read(4))

            fieldId = meta[0]
            nameLength = meta[2]
            type = FieldTypes(meta[1])

            if (fieldId != i):
                raise Exception('Field ordering invalid. File may be corrupted :(')

            name = self.file.read(nameLength).decode('utf8')

            self.fields.append({'name': name, 'type': type})
            print(self.fields)

    def readNext(self):
        buffer = self.file.read(4)
        if len(buffer) == 0:
            return None

        id = struct.unpack('<I', buffer)[0]
        if (id != self.sampleCounter):
            print(id)
            raise Exception('Sample count out of order. File may be corrupted :(')

        sample = {'id': id, 'captures': []}

        for i in range(0, len(self.fields)):
            field = self.fields[i]
            type = field['type']

            currentBuffer = self.file.read(2)
            recordedId = struct.unpack_from('<H', currentBuffer)[0]
            if (recordedId != i):
                raise Exception('Field captures out of order. File may be corrupted :(')

            currentBuffer += self.file.read(8 + type.size())
            capture = struct.unpack_from('<d' + type.format(), currentBuffer, 2)
            time = capture[0]
            data = capture[1]

            buffer += currentBuffer
            sample['captures'].append({'time': time, 'data': data})

        checksum = struct.unpack('<I', self.file.read(4))[0]

        if (Crc32.calc(buffer) != checksum):
            raise Exception('Sample checksum failed! File may be corrupted :(');

        self.sampleCounter += 1

        return sample
