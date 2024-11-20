# Общее описание
## Задание
Разработать ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Система команд УВМ представлена далее.

Для ассемблера необходимо разработать читаемое представление команд УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к которой задается из командной строки. Результатом работы ассемблера является бинарный файл в виде последовательности байт, путь к которому задается из командной строки. Дополнительный ключ командной строки задает путь к файлу-логу, в котором хранятся ассемблированные инструкции в духе списков “ключ=значение”, как в приведенных далее тестах.

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон также указывается из командной строки.
# Команды ассемблера
## Загрузка константы
| A | B | C |
| :---: | :---: | :---: |
| Биты 0-6 | Биты 7-13 | Биты 14-41 |
| 36 | Адрес | Константа |

Размер команды: 6 байт.

Операнд: поле C.

Результат: регистр по адресу, которым является поле B.
```
LOAD_CONSTANT 36 32 12
```
Байт-код для примера выше:
```0x24, 0x10, 0x03, 0x00, 0x00, 0x00 ```
## Чтение значения из памяти
| A | B | C |
| :---: | :---: | :---: |
| Биты 0-6 | Биты 7-13 | Биты 14-26 |
| 58 | Адрес | Адрес |

Размер команды: 6 байт.

Операнд: значение в памяти по адресу, которым является поле C.

Результат: регистр по адресу, которым является поле B.
```
READ_MEMORY 58 26 198
```
Байт-код для примера выше:
```0x3A, 0x8D, 0x31, 0x00, 0x00, 0x00 ```
## Запись значения в память
| A | B | C |
| :---: | :---: | :---: |
| Биты 0-6 | Биты 7-13 | Биты 14-26 |
| 25 | Адрес | Адрес |

Размер команды: 6 байт.

Операнд: регистр по адресу, которым является поле B.

Результат: значение в памяти по адресу, которым является поле C.
```
WRITE_MEMORY 25 48 919
```
Байт-код для примера выше:
```0x19, 0xD8, 0xE5, 0x00, 0x00, 0x00 ```
## Бинарная операция: умножение
| A | B | C | D |
| :---: | :---: | :---: | :---: |
| Биты 0-6 | Биты 7-13 | Биты 14-20 | Биты 21-27 |
| 32 | Адрес | Адрес | Адрес |

Размер команды: 6 байт.

Первый операнд: значение в памяти по адресу, которым является регистр по адресу, которым является поле C.

Второй операнд: регистр по адресу, которым является поле D.

Результат: регистр по адресу, которым является поле B.
```
MUL 32 68 90 15
```
Байт-код для примера выше:
```0x20, 0xA2, 0xF6, 0x01, 0x00, 0x00 ```
# Реализованный функционал
### grammar
Задается грамматика учебного конфигурационного языка для дальнейшего парсинга конфигурации.
### ConfigTransformer
Класс, в котором указываются правила преобразования каждого элемента из учебного конфигурационного языка. Все, реализованные в классе методы, в совокупности возвращают строку, содержащую конфигурацию на языке xml.
### parse_config
Функция парсит конфигурацию, поступившую на вход, по установленной ранее грамматике. Далее вызываются методы класса ConfigTransformer, благодаря чему поступившая конфигурация преобразуется в строку на языке xml. Помимо этого в функции реализован обработчик синтаксических ошибок.
### pretty_print_xml
Функция использует библиотеку xml.dom.minidom для преобразоваания строки на языке xml в красиво отформатированный файл на языке xml.
### main
Выполняется парсинг аргументов командной строки. Считывается конфигурация на учебном конфигурационном языке из стандартного потока ввода. Вызываются поочередно функции получения строки на языке xml и получения отформатированной строки на языке xml. Отформатированная строка записывается в файл, указанный ключом командной строки.
# Сборка и запуск проекта
1. Загрузить репозиторий на компьютер
```
git clone https://github.com/n1kpavlov/MIREA_assembler_and_interpreter
```
2. Прейдите в директорию репозитория
```
cd MIREA_assembler_and_interpreter
```
3. Запустить assembler.py с указанием исполняемой программы, бинарного файла вывода и лог-файла
```
py assembler.py <исполняемая_программа.asm> <бинарный_файл_вывода.bin> -l <лог-файл.xml>
```
4. Запустить interpreter.py с указанием бинарного файла данных, файла с результатами и диапазона памяти
```
py interpreter.py <бинарный_файл_данных.bin> <результат.xml> -lb <левая_граница_диапазона> -rb <правая граница диапазона>
```
# Примерs работы программы
### Настройка базы данных
**Входные данные:**
```
*> Configuring the database
def max_conn = 100
def timeout = 30
database {
    database = struct {
        host = 19216801,
        port = 5432,
        max_connections = [max_conn],
        connection_timeout = [timeout]
    }
}
```
**Выходные данные (XML):**
```
<?xml version="1.0" encoding="utf-8"?>
<database>
	<database type="dict">
		<host type="int">19216801</host>
		<port type="int">5432</port>
		<max_connections type="int">100</max_connections>
		<connection_timeout type="int">30</connection_timeout>
	</database>
</database>
```
### Конфигурация веб-приложения
**Входные данные:**
```
*> Web Application Configuration
def max_threads = 8
web_config {
    webserver = struct {
        hostname = 127001,
        port = 8080,
        threads = [max_threads],
        routes = struct {
            home = 1,
            login = 2,
            logout = 3
        }
    }
}
```
**Выходные данные (XML):**
```
<?xml version="1.0" encoding="utf-8"?>
<web_config>
	<webserver type="dict">
		<hostname type="int">127001</hostname>
		<port type="int">8080</port>
		<threads type="int">8</threads>
		<routes type="dict">
			<home type="int">1</home>
			<login type="int">2</login>
			<logout type="int">3</logout>
		</routes>
	</webserver>
</web_config>
```
### Конфигурация системы мониторинга
**Входные данные:**
```
*> Configuration of the monitoring system
def interval = 15
def retention = 365
monitoring_config {
    monitoring = struct {
        interval = [interval],
        retention_days = [retention],
        services = struct {
            first = 1,
            second = 2,
            third = 3,
            fourth = 4
        }
    }
}
```
**Выходные данные (XML):**
```
<?xml version="1.0" encoding="utf-8"?>
<monitoring_config>
	<monitoring type="dict">
		<interval type="int">15</interval>
		<retention_days type="int">365</retention_days>
		<services type="dict">
			<first type="int">1</first>
			<second type="int">2</second>
			<third type="int">3</third>
			<fourth type="int">4</fourth>
		</services>
	</monitoring>
</monitoring_config>
```
# Результаты тестирования
### Тест простой конфигурации
```
def test_simple_config(self):
	input_text = ('config {\n'
                      '\tsmth = 13\n'
                      '}\n')
        expected_output = '<config><smth type="int">13</smth></config>'
        self.assertEqual(parse_config(input_text), expected_output)
```
### Тест словаря
```
def test_dict(self):
	input_text = ('config {\n'
                      '\tnames = struct {\n'
                      '\t\tnikita = 1,\n'
                      '\t\tartem = 2\n'
                      '\t}\n'
                      '}\n')
        expected_output = '<config><names type="dict"><nikita type="int">1</nikita><artem type="int">2</artem></names></config>'
        self.assertEqual(parse_config(input_text), expected_output)
```
### Тест константы
```
def test_constant(self):
        input_text = ('def x = 5\n'
                      'config {\n'
                      '\tsmth = [x]\n'
                      '}\n')
        expected_output = '<config><smth type="int">5</smth></config>'
        self.assertEqual(parse_config(input_text), expected_output)
```
### Тест комментария
```
def test_comment(self):
        input_text = ('*> comment\n'
                      'config {\n'
                      '\tsmth = 10\n'
                      '}\n')
        expected_output = '<config><smth type="int">10</smth></config>'
        self.assertEqual(parse_config(input_text), expected_output)
```
### Тест синтаксической ошибки
```
def test_syntax_error(self):
        input_text = ('def x = 5\n'
                      'config {\n'
                      '\tsmth = x\n'
                      '}\n')
        result = parse_config(input_text)
        assert "Unexpected Characters" in result
```
### Тест использования необъявленной константы
```
def test_undefined_constant_error(self):
        input_text = ('config {\n'
                      '\tsmth = [undefined_constant]\n'
                      '}\n')
        result = parse_config(input_text)
        assert "В конфигурации использована неизвестная константа по имени undefined_constant" in result
```
### Тест повторного объявления константы
```
def test_duplicate_constant_error(self):
        input_text = ('def x = 5\n'
                      'def x = 10\n'
                      'config {\n'
                      '\tsmth = [x]\n'
                      '}\n')
        result = parse_config(input_text)
        assert "Константа x уже объявлена" in result
```
### Тест форматированного вывода
```
def test_output_xml(self):
        input_text = ('*> Test comment\n'
                      'def int = 10\n'
                      'main {\n'
                      '\tcombo = struct {\n'
                      '\t\tnumber = 19216801,\n'
                      '\tmax_connections = [int]\n'
                      '\t}\n'
                      '}\n')
        expected_output = ('<?xml version="1.0" encoding="utf-8"?>\n'
                        '<main>\n'
                        '\t<combo type="dict">\n'
                        '\t\t<number type="int">19216801</number>\n'
                        '\t\t<max_connections type="int">10</max_connections>\n'
                        '\t</combo>\n'
                        '</main>\n')
        self.assertEqual(pretty_print_xml(parse_config(input_text)), expected_output)
```
![image](https://github.com/user-attachments/assets/4f180366-0af7-44be-81a5-15770bd454dc)
