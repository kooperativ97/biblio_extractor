'''
FDT Reader reads an FDT File from a CDS/ISIS Database and 
converts it into a dictionary to connect column names to field
defintions.
'''
class FDTReader():

    def __init__(self):
        pass

    def _readFileAsLines(self, path) -> list:
        lines = []
        with open(path, "r", encoding="utf-8", errors="backslashreplace") as file:
            lines = file.readlines()
        
        cut = 0
        for line in lines:
            if "***" in line:
                cut += 1
                break
            cut += 1 

        return lines[cut:]

    '''
    ä   \x84    Ä   \x8E
    ö   \x94    Ö   \x99
    ü   \x81    Ü   \x9A
    '''
    def _umlaut_replace(self, text: str) -> str:
        text =  text.replace('\\x84', 'ä')\
                    .replace('\\x81', 'ü')\
                    .replace('\\x94', 'ö')\
                    .replace('\\x99', 'Ö')\
                    .replace('\\x8E', 'Ä')\
                    .replace('\\x9A', 'Ü')\
                    .replace('\\x9a', 'Ü')\
                    .replace('\\xe1', 'ß')
        return text

    def getDictionary(self, path: str, add_subfields=False) -> dict:
        lines = self._readFileAsLines(path)
        columns = dict()
        for line in lines: 
            line = self._umlaut_replace(line)
            name =line[0:30].strip()
            subfields = line[30:48].strip()
            field_number = line[48:].strip().split(" ")[0]
            if add_subfields: 
                for subf in subfields:
                    columns[f"{field_number}_{subf}"] = name
            
            columns[field_number] = name
        return columns
    
    def generatePFT(self, path, column_delimiter="|||", entry_delimiter="###") -> str: 
        d = self.getDictionary(path)
        pft = f''
        for k in d.keys():
            pft += f'"v{k}: "v{k}"{column_delimiter}",'

        #remove last ","
        if pft[-1] == ",":
            pft = pft[0:len(pft)-1]

        pft = pft[0] + entry_delimiter + pft[1:len(pft)]
        
        return pft
        

if __name__ == "__main__":
    print(FDTReader().getDictionary("data/BIBLIO.FDT", True))
    print(FDTReader().generatePFT("data/BIBLIO.FDT"))
