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
        if (A != 36):
            raise ValueError("Параметр А должен быть равен 36")
        if not (0 <= B < (1 << 7)):
            raise ValueError("Адрес B должен быть в пределах от 0 до 2^7-1")
        if not (0 <= C < (1 << 28)):
            raise ValueError("Константа C должна быть в пределах от 0 до 2^28-1")

        bits = (C << 14) | (B << 7) | A
        bits = bits.to_bytes(6, byteorder="little")
            
        return bits

    def read_memory(self, A, B, C):
        if (A != 58):
            raise ValueError("Параметр А должен быть равен 58")
        if not (0 <= B < (1 << 7)):
            raise ValueError("Адрес B должен быть в пределах от 0 до 2^7-1")
        if not (0 <= C < (1 << 13)):
            raise ValueError("Адрес C должен быть в пределах от 0 до 2^13-1")

        bits = (C << 14) | (B << 7) | A
        bits = bits.to_bytes(6, byteorder="little")
            
        return bits

    def write_memory(self, A, B, C):
        if (A != 25):
            raise ValueError("Параметр А должен быть равен 25")
        if not (0 <= B < (1 << 7)):
            raise ValueError("Адрес B должен быть в пределах от 0 до 2^7-1")
        if not (0 <= C < (1 << 13)):
            raise ValueError("Адрес C должен быть в пределах от 0 до 2^13-1")

        bits = (C << 14) | (B << 7) | A
        bits = bits.to_bytes(6, byteorder="little")
            
        return bits

    def multiply(self, A, B, C, D):
        if (A != 32):
            raise ValueError("Параметр А должен быть равен 32")
        if not (0 <= B < (1 << 7)):
            raise ValueError("Адрес B должен быть в пределах от 0 до 2^7-1")
        if not (0 <= C < (1 << 7)):
            raise ValueError("Адрес C должен быть в пределах от 0 до 2^7-1")
        if not (0 <= D < (1 << 7)):
            raise ValueError("Адрес D должен быть в пределах от 0 до 2^7-1")

        bits = (D << 21) | (C << 14) | (B << 7) | A
        bits = bits.to_bytes(6, byteorder="little")
            
        return bits

    def assemble(self):
        with open(self.code_path, "rt") as code:
            for line in code:
                line = line.split('\n')[0].strip()
                if not line: continue

                command, *args = line.split()

                match command:
                    case "LOAD_CONSTANT":
                        if len(args) != 3:
                            raise SyntaxError(
                                f"{line}\nУ операции загрузки константы должно быть 3 аргумента")
                        
                        self.bytes.append(self.load_constant(int(args[0]), int(args[1]), int(args[2])))

                    case "READ_MEMORY":
                        if len(args) != 3:
                            raise SyntaxError(
                                f"{line}\nУ операции чтении из памяти должно быть 3 аргумента")
                        
                        self.bytes.append(self.read_memory(int(args[0]), int(args[1]), int(args[2])))

                    case "WRITE_MEMORY":
                        if len(args) != 3:
                            raise SyntaxError(
                                f"{line}\nУ операции чтении из памяти должно быть 3 аргумента")
                            
                        self.bytes.append(self.write_memory(int(args[0]), int(args[1]), int(args[2])))

                    case "MUL":
                        if len(args) != 4:
                            raise SyntaxError(
                                f"{line}\nУ операции умножения должно быть 4 аргумента")
                        
                        self.bytes.append(self.multiply(int(args[0]), int(args[1]), int(args[2]), int(args[3])))

                    case _:
                        raise SyntaxError(f"{line}\nНеизвестная команда")

        self.to_binary_file()

    def to_binary_file(self):
        with open(self.binary_file_path, "wb") as binary:
            for byte in self.bytes:
                binary.write(byte)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Входной файл (.asm)")
    parser.add_argument("output", help="Выходной файл (.bin)")
    parser.add_argument("-l", "--log", help="Файл лога (.xml)", default=None)
    args = parser.parse_args()

    assembler = Assembler(args.input, args.output, args.log)
    try:
        assembler.assemble()
    except ValueError as e:
        print(e)
    print(f"Ассемблирование выполнено успешно. Выходной файл: {args.output}")
