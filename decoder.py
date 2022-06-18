import re
import chardet
from more_itertools import partitions
from transformers import CharSpan
from entry import Entry

USE_ONLY_SUB_SAMPLE = False

#this list contains the ords for the text found in each entry
OKAY_ORDS = [e for e in range(32, 160)]

strdata = None

if False:
    with open("data/BIBLIO.MST", "rb") as file: 
        bdata = file.read()
        print(chardet.detect(bdata[1000:100000]))

with open("data/backup/BIBLIO.MST", "r", encoding="latin-1") as file: 
    strdata = file.read()

if USE_ONLY_SUB_SAMPLE:
  strdata = strdata[100000:1000000]

#matches an entry (with start and end tokens)
#this expression is optimistic, it will match some false positives
entry_pattern = re.compile(r"((\t\x00)(.|\n)*?(\x00\x00))") 

# remove all characters that are not meant to be in the data
def cut(text: str) -> str:
    return "".join([t for t in text if ord(t) in OKAY_ORDS])

#go through all matches, clean them and add them to the list
entries = []
for i, match in enumerate(re.findall(entry_pattern, strdata)):
    match = [cut(e) for e in match]
    entry = [e for e in match if len(e) > 1]
    if len(entry) == 0 :
        continue #skip empty matches
    elif len(entry) > 1:
        #if there are multiple matches (which can happen sometime)
        #order by length and take the longest one
        entry = entry.sort(key=lambda x: len(x), reverse=True)
    
    ent = Entry(i, entry[0])
    entries.append(ent)

#Filter out small entries
#entries = [l for l in entries if len(l) > 20]

print(f"{len(entries)} entries found")


# split each entry by the possible subfields

field_delimiter_pattern = re.compile(r"\^[\w]")
splitted_lines = []

'''
ä   \x84    Ä   \x8E
ö   \x94    Ö   \x99
ü   \x81    Ü   \x9A
'''
def umlaut_replace(text: str) -> str:
    text =  text.replace('\x84', 'ä')\
                .replace('\x81', 'ü')\
                .replace('\x94', 'ö')\
                .replace('\x99', 'Ö')\
                .replace('\x8E', 'Ä')\
                .replace('\x9A', 'Ü')\
                .replace('\xe1', 'ß')
    return text


def wierd(text: str) -> bool:
    chars = 0
    special = 0
    numbers = 0
    chs = set()
    penalty = 1
    for l in text:
        if ord(l) > 32 and ord(l) < 47:
            special += 1 
        elif ord(l) >= 47 and ord(l) <=57:
            numbers += 1
        elif ord(l) >= 58 and ord(l) <=64:
            special += 1
        elif ord(l) >= 91 and ord(l) <= 96:
            special += 1
        elif ord(l) >= 123 and ord(l) <= 126:
            special += 1
        else: 
            chars += 1
            chs.add(l)

    if len(chs) * 3 > chars or chars == 1:
        penalty = 10

    return ( (special + numbers) / (chars + 1) ) * len(text) * penalty > 8

#split by delimiters and remove the first entry which is always glibberish (due to the regex match that matches too optimistic)
#also replace umlauts 
for ent in entries:
    parts = field_delimiter_pattern.split(ent.getUncutText())
    parts = [umlaut_replace(p) for p in parts if not chr(0) in p]
    if len(parts[0]) > 1:
        if wierd(parts[0]):
            if parts[0][-1] != "M":
                parts = parts[1:]
            else:
                parts[0] = parts[0][-1] 
    i_to_del = set()
    for i, p in enumerate(parts): 
        for c in p:
            if ord(c) > 127 and ord(c) < 160:
                if "präsent" not in p:
                    i_to_del.add(i)
                    #print(f"{c} found with code {ord(c)}: removing {p} with index {i}")
                    continue
    if len(i_to_del):
        pass #print(parts)
    for index in sorted(i_to_del, reverse=True):
        pass #del parts[index] #delete in reverse order to keep indexes
    parts = [p for p in parts if len(p) > 0]
    ent._arr = parts




#print to file
with open("BIBLIO_ENTRIES_backup.txt", "w", encoding="utf-8") as f:
    for l in entries: 
        print(l, file=f)


print("Converting to set")
entries = [ele for ind, ele in enumerate(entries) if ele not in entries[:ind]]


with open("BIBLIO_ENTRIES_SET_backup.txt", "w", encoding="utf-8") as f:
    for l in entries: 
        print(l, file=f)




'''
 M. zahlr. Ill. --> Mit zahlreichen Illustrationen
 

'''
