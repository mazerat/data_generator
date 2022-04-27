# Описание работы
Инструмент представляет из себя набор Python скриптов для генерации файлов данных
со статистикой потребления абстрактного ресурса зарегистриованными пользователями
и последующей обработки и записи аггрерированной статистики в базу данных.

## Использование "data_generator"
Скрипт используется для генерации файлов данных.
Работает в режиме консольного приложения.

```sh
[kirill@archlinux resource_calculator]$ python data_generator.py --help
Usage: data_generator.py [OPTIONS]

  Main function for module. Accepts command line parameters.

  :param output_folder: Folder path where new file will be created.   
  :param files_amount: Number of files to be created in output_folder.  
  :param records_amount: Lines amount in each file created. :return: None.

Options:
  --output_folder TEXT      Output folder where generated files are stored
  --files_amount INTEGER    Number of files to be generated
  --records_amount INTEGER  Number of records per each file
  --help                    Show this message and exit.
```

В результате работы скрипта будут сгенерированы файлы данных в количестве,
соответствующем значению `--files_amount` и помещены в папку, соответствующую
значению `--output_folder`. В каждом файле будет `--records_amount` строк.

## Использование "data_parser"
Скрипт используется для парсинга сгенериованных файлов и загрузки данных в
базу. Работает в режиме долгоживущего процесса.

```sh
[kirill@archlinux resource_calculator]$ python data_parser.py --help
Usage: data_parser.py [OPTIONS]

  Main function for module. Accepts command line parameters.

  :param data_files_folder: Folder path where data files are stored.   
  :param backup_directory: Folder to place parsed files for backup.   
  :param database_file: Full path to SQLLite database file.    
  :param map_max_size: Max amount of key-value pairs accumulated before dumping to database

Options:
  --data_files_folder TEXT  Folder where data files are stored
  --backup_directory TEXT   Folder where processed files are backed up
  --database_file TEXT      SQLite database file path
  --map_max_size INTEGER    Max amount of key-value pairs accumulated before
                            dumping to database
  --help                    Show this message and exit.
```

В результате работы скрипта дата файлы из папки `--data_files_folder` будут прочитаны,
данные из них агрегированны по каждому пользователю и записаны в базу данных.
Сами файлы данных будут перемещены в папку, соответствующую значению
`--backup_directory`.   
В качестве демонстрации работоспособности решения используется локальная база данных
SQLLite. Файл базы данных будет доступен в папке, соответствующей значению
`--database_file` параметра.

## Запуск тестов
Unit тесты находятся в папке resource_calculator/tests. Запустить их можно из папки
resource_calculator:

```sh
[kirill@archlinux resource_calculator]$ python -m unittest tests/test_resource_calculator_utils.py -v
test_create_data_files_directory (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... ok
test_get_first_file_in_folder (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... ok
test_move_file (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... 2022-04-28 00:13:07,884 - [INFO] - utils.resource_calculator_utils - (resource_calculator_utils.py).move_file(85) - Moving temporary file /tmp/8fd0c2b7badd493dbae0797ce2fc5ce1 to permanent location /tmp/6ee0061b5c8a4744ad80f36459f0de44
2022-04-28 00:13:07,884 - [INFO] - utils.resource_calculator_utils - (resource_calculator_utils.py).move_file(88) - Successfully moved file "/tmp/6ee0061b5c8a4744ad80f36459f0de44"
ok
test_numbers_amount_0 (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... ok
test_numbers_amount_1 (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... ok
test_numbers_amount_2 (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... ok
test_numbers_amount_3 (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... ok
test_numbers_amount_4 (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... ok
test_numbers_amount_negative (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... ok
test_unique_filename_generation (tests.test_resource_calculator_utils.TestResourceCalculatorUtils) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.002s

OK
[kirill@archlinux resource_calculator]$
```
