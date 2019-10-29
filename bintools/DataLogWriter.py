import struct
import time
import subprocess

from crccheck.crc import Crc32
from . import FieldTypes

class DataLogWriter:
    def __init__(self, filename, fields):
        assert isinstance(filename, str)
        assert isinstance(fields, list)

        self.sampleCounter = 0
        self.collecting = False

        self.filename = filename
        self.file = open(filename, 'xb', 0)
        self.fields = fields
        self.__writeHeader()

    def __writeHeader(self):
        magic = bytes('NC🚀2019', 'utf-8')
        fieldsLength = struct.pack('<H', len(self.fields))
        self.file.write(magic)
        self.file.write(fieldsLength)

        for i in range(0, len(self.fields)):
            field = self.fields[i]
            name = field['name']
            type = field['type']

            encodedName = name.encode('utf8')
            meta = struct.pack('<HBB', i, type.value, len(encodedName))

            self.file.write(meta)
            self.file.write(encodedName)

        self.file.flush()

    def __writeSamplePacket(self):
        if len(self.currentCapture) != len(self.fields):
            raise Exception('Captured data does not match number of fields.')

        samplePacket = bytes()

        # Sample ID
        samplePacket += struct.pack('<I', self.sampleCounter)

        # Fields
        for i in range(0, len(self.fields)):
            field = self.fields[i]
            sample = self.currentCapture[i]

            type = field['type']
            data = sample['data']
            time = sample['time']

            samplePacket += struct.pack('<Hf' + type.format(), i, time, data)

        # CRC32
        samplePacket += struct.pack('<I', Crc32.calc(samplePacket))

        self.file.write(samplePacket)
        self.file.flush()

        if self.sampleCounter % 500 == 0:
            subprocess.Popen(['/bin/sync', '-d', self.filename]) # Force changes to disk

    def beginSample(self):
        if self.collecting:
            raise Exception('Cannot start secondary sample collection during sample collection.')

        self.collecting = True
        self.currentCapture = []

    def close(self):
        self.file.close()

    def endSample(self):
        if not self.collecting:
            raise Exception('No sample collection started.')

        self.__writeSamplePacket()
        self.collecting = False
        self.sampleCounter += 1

    def log(self, data):
        if not self.collecting:
            raise Exception('Cannot log data outside of sample.')

        self.currentCapture.append({'data': data, 'time': time.time()})
