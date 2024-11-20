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

    def load_constant(self, A, B, C):
        
        return bits

    def read_memory(self, A, B, C):
       
        return bits

    def write_memory(self, A, B, C):
        
        return bits

    def multiply(self, A, B, C, D):
        
        return bits

    def assemble(self):
        with open(self.code_path, "rt") as code:
            for line in code:
                line = line.split('\n')[0].strip()
                if not line: continue

                command, *args = line.split()

                match command:
                    case "LOAD_CONSTANT":                    
                        self.bytes.append(self.load_constant(int(args[0]), int(args[1]), int(args[2])))

                    case "READ_MEMORY":
                        self.bytes.append(self.read_memory(int(args[0]), int(args[1]), int(args[2])))

                    case "WRITE_MEMORY":                        
                        self.bytes.append(self.write_memory(int(args[0]), int(args[1]), int(args[2])))

                    case "MUL":
                        self.bytes.append(self.multiply(int(args[0]), int(args[1]), int(args[2]), int(args[3])))

                    case _:
                        raise SyntaxError(f"{line}\nНеизвестная команда")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Входной файл (.asm)")
    parser.add_argument("output", help="Выходной файл (.bin)")
    parser.add_argument("-l", "--log", help="Файл лога (.xml)", default=None)
    args = parser.parse_args()

    assembler = Assembler(args.input, args.output, args.log)
    assembler.assemble()
    
    print(f"Ассемблирование выполнено успешно. Выходной файл: {args.output}")
