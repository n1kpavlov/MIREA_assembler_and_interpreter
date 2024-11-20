import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom

class Assembler:
    def __init__(self, path_to_code, path_to_binary_file, path_to_log):
        self.binary_file_path = path_to_binary_file
        self.code_path = path_to_code
        self.log_path = path_to_log

        self.bytes = []
        self.log_root = ET.Element("log")

    def assemble(self):
        with open(self.code_path, "rt") as code:
            for line in code:
                line = line.split('\n')[0].strip()
                if not line: continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Входной файл (.asm)")
    parser.add_argument("output", help="Выходной файл (.bin)")
    parser.add_argument("-l", "--log", help="Файл лога (.xml)", default=None)
    args = parser.parse_args()

    assembler = Assembler(args.input, args.output, args.log)
    assembler.assemble()
    
    print(f"Ассемблирование выполнено успешно. Выходной файл: {args.output}")
