'''
DataReader reads an ASCII File exported from a CDS/ISIS Database and 
'''

class DataReader():

    def __init__(self, field_delimiter="|||", entry_delimiter="###"):
        self._field_delimiter = field_delimiter
        self._entry_delimiter = entry_delimiter

        
    def _read_lines(self, path: str) -> list: 
        lines = []
        with open(path, "r", encoding="utf8", errors="backslashreplace") as file:
            lines = file.readlines()

        line = " ".join(lines)
        entries = line.split("###")

        for i, e in enumerate(entries):
            entries[i] = e.split("|||")

        for i, e in enumerate(entries):
            entries[i] = [a.encode().decode('unicode_escape') for a in e]
        
        return [e for e in entries if len(e) > 2]


    def getData(self, path: str):
        return self._read_lines(path)



if __name__ == "__main__":
    DataReader().getData("data/prints/export.txt")