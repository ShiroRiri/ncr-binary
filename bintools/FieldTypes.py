from enum import Enum

class FieldTypes(Enum):
    UINT_8 = 0
    UINT_16 = 1
    UINT_32 = 2
    INT_8 = 3
    INT_16 = 4
    INT_32 = 5
    FLOAT = 6
    DOUBLE = 7
    STRING = 8
    
    @classmethod
    def formatOf(cls, type):
        formatMap = {
            cls.UINT_8: 'B',
            cls.UINT_16: 'H',
            cls.UINT_32: 'I',
            cls.INT_8: 'b',
            cls.INT_16: 'h',
            cls.INT_32: 'i',
            cls.FLOAT: 'f',
            cls.DOUBLE: 'd',
            cls.STRING: 'p'
        }
        
        return formatMap[type]

    @classmethod
    def sizeOf(cls, type):
        sizeMap = {
            cls.UINT_8: 1,
            cls.UINT_16: 2,
            cls.UINT_32: 4,
            cls.INT_8: 1,
            cls.INT_16: 2,
            cls.INT_32: 4,
            cls.FLOAT: 4,
            cls.DOUBLE: 8,
            cls.STRING: -1
        }
        
        return sizeMap[type]

    def size(self):
        return self.sizeOf(self)
        
    def format(self):
        return self.formatOf(self)
