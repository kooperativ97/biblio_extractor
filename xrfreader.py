from tarfile import BLOCKSIZE

def convert_to_bits(f):
    for b in f:
        for i in range(8):
            yield str((b >> i) & 1)

BLOCK_SIZE = 512
POINTER_SIZE = 32
bdata = None

with open("data/BIBLIO.XRF", "rb") as file: 
    bdata = file.read()

blocks = int(len(bdata)/BLOCK_SIZE)

print(f"The XRF File has {len(bdata)} bytes with {blocks} blocks")

for i in range(0, blocks):
    block_start = i * BLOCK_SIZE
    block_end = (i + 1) * BLOCK_SIZE
    chunk = bdata[block_start : block_end]
    bits = [b for b in convert_to_bits(chunk)]
    print(f"{len(chunk)}, {len(bits)}")
    pointers = []
    for j in range(1, int(len(bits)/POINTER_SIZE)):
        pointer_start = j * POINTER_SIZE
        pointer_end = (j + 1) * POINTER_SIZE
        XRFMFB = int("".join(bits[pointer_start:pointer_start+21]), 2)
        XRFMFP = int("".join(bits[pointer_start+21:pointer_end]), 2)
        pointer = XRFMFB * 2048 + XRFMFP
        pointers.append(pointer)
    print(f"{len(pointers)} pointers")
    print(pointers)
    print()

    