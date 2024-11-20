import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom

class Interpreter:
    def __init__(self, path_to_binary_file, left_boundary, right_boundary, path_to_result_file):
        self.result_path = path_to_result_file
        self.boundaries = (left_boundary, right_boundary)
        self.registers = [0] * (right_boundary - left_boundary + 1)

        with open(path_to_binary_file, 'rb') as binary_file:
            self.byte_code = int.from_bytes(binary_file.read(), byteorder="little")

    def interpret(self):
        while self.byte_code != 0:
            a = self.byte_code & ((1 << 7) - 1)
            self.byte_code >>= 7
            match a:
                case 36:
                    self.load_constant()
                case 58:
                    self.read_memory()
                case 25:
                    self.write_memory()
                case 32:
                    self.mul()
                case _:
                    raise ValueError("В бинарном файле содержатся невалидные данные: неверный байт-код")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Входной бинарный файл")
    parser.add_argument("output", help="Выходной XML файл")
    parser.add_argument("-lb", "--left_boundary", help="Левая граница памяти", default=0)
    parser.add_argument("-rb", "--right_boundary", help="Правая граница памяти", default=8191)
    args = parser.parse_args()
    
    interpreter = Interpreter(args.input, int(args.left_boundary), int(args.right_boundary), args.output)
        try:
        interpreter.interpret()
    except ValueError as e:
        print(e)
    print(f"Интерпретация выполнена успешно. Результаты сохранены в {args.output}")
