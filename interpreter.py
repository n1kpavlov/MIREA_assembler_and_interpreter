import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Входной бинарный файл")
    parser.add_argument("output", help="Выходной XML файл")
    parser.add_argument("-lb", "--left_boundary", help="Левая граница памяти", default=0)
    parser.add_argument("-rb", "--right_boundary", help="Правая граница памяти", default=8191)
    args = parser.parse_args()
