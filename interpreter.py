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

        self.make_result()

    def load_constant(self):
        B = self.byte_code & ((1 << 7) - 1)
        self.byte_code >>= 7
        C = self.byte_code & ((1 << 28) - 1)
        self.byte_code >>= 34

        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")

        self.registers[B] = C

    def read_memory(self):
        B = self.byte_code & ((1 << 7) - 1)
        self.byte_code >>= 7
        C = self.byte_code & ((1 << 13) - 1)
        self.byte_code >>= 34

        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= C <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")

        self.registers[B] = self.registers[C]

    def write_memory(self):
        B = self.byte_code & ((1 << 7) - 1)
        self.byte_code >>= 7
        C = self.byte_code & ((1 << 13) - 1)
        self.byte_code >>= 34

        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= C <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")

        self.registers[C] = self.registers[B]

    def mul(self):
        B = self.byte_code & ((1 << 7) - 1)
        self.byte_code >>= 7
        C = self.byte_code & ((1 << 7) - 1)
        self.byte_code >>= 7
        D = self.byte_code & ((1 << 7) - 1)
        self.byte_code >>= 27

        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= C <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= D <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")

        self.registers[B] = self.registers[C] * self.registers[D]

    def make_result(self):
        result_root = ET.Element("result")
        for pos, register in enumerate(self.registers, self.boundaries[0]):
            if (register != 0):
                element = ET.SubElement(result_root, "register")
                element.attrib['address'] = str(pos)
                element.text = str(register)

        log_data = ET.tostring(result_root, encoding="unicode", method="xml").encode()
        dom = xml.dom.minidom.parseString(log_data)
        log = f'<?xml version="1.0" encoding="utf-8"?>\n' + dom.toprettyxml(newl="\n")[23:]
        with open(self.result_path, 'w', encoding='utf-8') as f:
            f.write(log)


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
