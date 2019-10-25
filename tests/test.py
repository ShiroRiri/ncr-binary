from bintools import DataLogWriter, DataLogReader, FieldTypes

writer = DataLogWriter('/tmp/test-write.bin', [
    {'name': 'TestField-01', 'type': FieldTypes.UINT_32}
])

for i in range(0, 5000):
    writer.beginSample()
    writer.log(i)
    writer.endSample()

writer.close()

reader = DataLogReader('/tmp/test-write.bin')
