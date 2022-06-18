'''
Combiner combines the FDT Dictionary with the Data read by DataReader
'''
from DataReader import DataReader
from FDTReader import FDTReader
import re 
import json

class Combiner():

    def __init__(self, fdt_path:str, data_path:str):
        self._columns = FDTReader().getDictionary(fdt_path)
        self._data = DataReader().getData(data_path) 
        
    def _dictiofy(self) -> list:
        entries = []
        for entry in self._data:
            entryd = dict()
            for element in entry:
                #checks if string starts with v\d+
                column = re.findall(r"^(v[0-9]+):.*", element)
                if not column:
                    continue
                else:
                    column = column[0]
                    #if yes, check if the format is column: data
                    if re.match(r"^v[0-9]+:.*", element):
                        #match only the data (negative look-behind has to be fixed length, so we match a tuple of three vor v1, v10 and v100 cases)
                        data = re.findall(r"(?<=v[0-9]:)(.*)|(?<=v[0-9][0-9]:)(.*)|(?<=v[0-9][0-9][0-9]:)(.*)", element)
                        data = [a for a in data[0] if a] #only take the matched part
                        entryd[column] = data[0].strip() #strip and save
            entries.append(entryd)
        return entries

    def _explode_to_subfields(self, d: dict) -> dict: 
        newd = dict()
        for k, v in d.items():
            subs = re.findall(r"\^([\w])", v)

            #if there are subfields add them as sub dictionary
            if len(subs) > 0:
                field_delimiter_pattern = re.compile(r"\^[\w]")
                value_parts = field_delimiter_pattern.split(v)
                if len(value_parts) > 0:
                    value_parts = value_parts[1:]
                
                value_dict = dict()

                for s, vp in zip(subs, value_parts):
                    if vp: #only save if there is actually data
                        value_dict[s] = vp

                if value_dict.keys():
                    newd[k] = value_dict
                
            else:
                newd[k] = v

        return newd
            

    def _humanize_columns(self, d: dict) -> dict: 
        newd = dict()
        for k, v in d.items():
            new_key = self._columns[k.replace("v", "")]
            if v:
                newd[new_key] = v
        return newd


    def combine(self):
        entries = self._dictiofy()
        entries = [self._explode_to_subfields(d) for d in entries]
        entries = [self._humanize_columns(d) for d in entries]
        return entries

    def save_json(self, path):
        with open(path, 'w') as fp:
            json.dump(self.combine(), fp)

if __name__ == "__main__":
    combiner = Combiner("data/BIBLIO.FDT", "data/prints/export.txt")
    combiner.save_json("data.json")