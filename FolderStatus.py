from enum import IntEnum

class FolderStatus(IntEnum):
    NONE = 0
    ADDED = 1
    REMOVED = 4
    CONFIRMEDREMOVED = 5
    MOVEDORRENAMED = 6
    
