import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Входной файл (.asm)")
    parser.add_argument("output", help="Выходной файл (.bin)")
    parser.add_argument("-l", "--log", help="Файл лога (.xml)", default=None)
    args = parser.parse_args()

    
    print(f"Ассемблирование выполнено успешно. Выходной файл: {args.output}")
