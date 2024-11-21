import unittest
import os
from assembler import Assembler
from interpreter import Interpreter

class TestAssembler(unittest.TestCase):
    def test_load_const(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("LOAD_CONSTANT 36 32 12")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "241003000000")

    def test_read_memory(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("READ_MEMORY 58 26 198")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "3a8d31000000")

    def test_write_memory(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("WRITE_MEMORY 25 48 919")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "19d8e5000000")

    def test_multiply(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("MUL 32 68 90 15")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "20a2f6010000")

    def test_value_error(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("LOAD_CONSTANT 10 10 10")

        assembler = Assembler(filename, binary_file, log_file)
        with self.assertRaisesRegex(ValueError, "Параметр А должен быть равен 36"):
            assembler.assemble()

        os.remove(filename)

    def test_syntax_error(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("MOV 50")

        assembler = Assembler(filename, binary_file, log_file)
        with self.assertRaisesRegex(SyntaxError, "Неизвестная команда"):
            assembler.assemble()

        os.remove(filename)

class TestInterpreter(unittest.TestCase):
    def test_load_const(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x24\x10\x03\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[32], 12)

    def test_read_memory(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x3a\x8d\x31\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[26], 0)

    def test_write_memory(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x19\xd8\xe5\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[919], 0)

    def test_multiply(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x20\xa2\xf6\x01\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[68], 0)

    def test_value_error(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x01\x00\x00\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        with self.assertRaisesRegex(ValueError, "В бинарном файле содержатся невалидные данные: неверный байт-код"):
            interpreter.interpret()

        os.remove(filename)

        self.assertEqual(interpreter.registers[919], 0)

if __name__ == '__main__':
    unittest.main()
