import argparse 
from Combiner import Combiner
from FDTReader import FDTReader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Exporter for CDS/ISIS database prints')
    parser.add_argument("--generate", "-g", choices=['pft','json'], default = 'json')
    parser.add_argument('--output-file', "-o", type=str, required=True)
    parser.add_argument('--fdt-file', "-fdt", type=str, required=True)
    parser.add_argument('--export-file', "-epf", type=str, required=False)

    args = parser.parse_args()

    if args.generate == "pft":
        fdt = FDTReader().generatePFT(args.fdt_file)
        with open(args.output_file, "w") as f:
            f.write(fdt)

        exit(0)

    else:
        if args.export_file is None: 
            parser.error("File path for export is needed to generate the json file.")
            exit(1)

        combiner = Combiner(args.fdt_file, args.export_file)
        combiner.save_json(args.output_file)    
        exit(0)



'''
Generate PFT File containing all the columns from the FDT

> python export.py -g pft -fdt data/BIBLIO.FDT -o FORMAT.PFT


Generate JSON File from fullexport.txt and the FDT 

> python export.py -g json -fdt data/BIBLIO.FDT -epf data/prints/fullexport.txt -o export.json




'''