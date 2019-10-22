from bintools import DataLogWriter, FieldTypes

writer = DataLogWriter('/tmp/test-write.bin', [
    {'name': 'TestField-01', 'type': FieldTypes.UINT_8}
])
