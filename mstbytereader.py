from tarfile import BLOCKSIZE
import subprocess
from subprocess import CalledProcessError

def convert_to_bits(f):
    for b in f:
        for i in range(8):
            yield str((b >> i) & 1)

BLOCK_SIZE = 512
bdata = None

with open("data/BIBLIO.MST", "rb") as file: 
    bdata = file.read()

rbdata = bdata[::-1]

code = 1

while(code == 1):
    with open("data/BIBLIO_PART.MST", "wb") as file:
        file.write(rbdata[0:(BLOCK_SIZE*10)])

    try:
        code = subprocess.check_output(['ioisis', 'mst2csv', 'data/BIBLIO_PART.MST'])
        print(err)
    except CalledProcessError as err:
        code = err.args[0]

blocks = int(len(bdata)/BLOCK_SIZE)



print(f"The MST File has {len(bdata)} bytes with {blocks} blocks")
exit(0)
for i in reversed(range(0, blocks)):
    block_start = (i - 1) * BLOCK_SIZE
    block_end =         i * BLOCK_SIZE
    chunk = bdata[block_start : block_end]
    bits = [b for b in convert_to_bits(chunk)]
    print(f"{len(chunk)}, {len(bits)}")

    