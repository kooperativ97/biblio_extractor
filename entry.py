from ast import Str


class Entry():
    _nr = None
    _uncut_text = None
    _arr = None

    def __init__(self, nr: int, uncut: str):
        self._nr = nr
        self._uncut_text = uncut 

    
    def getUncutText(self) -> str: 
        return self._uncut_text

    def getArray(self) -> str:
        return self._arr
    
    def similarity(entry) -> float:

        return 0

    def __len__(self) -> int:
        return len(self._arr)

    def __repr__(self) -> str:
        return f"[E{self._nr:05d}] with {len(self._arr):02d} fields: {self._arr}"

    def __str__(self) -> str:
        return f"[E{self._nr:05d}] with {len(self._arr):02d} fields: {self._arr}"