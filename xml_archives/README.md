## Description

Write a Python program that does the following:
1. Creates 50 zip archives, each containing 100 xml files with random data of the following structure:
```xml
<root>
<var name='id' value='<random unique string>'/>
<var name='level' value='<random number from 1 to 100>'/>
<objects>
<object name='<random string>'/>
<object name='<random string>'/>
…
</objects>
</root>
```
2. Processes the directory with received zip archives, parses nested xml files and generates 2 csv files
   * `levels.csv`: `id, level` - one line for each xml file
   * `objects.csv`: `id, object_name` - a separate line for each object tag (from 1 to 10 lines for each xml file)

It is desirable that task 2 uses the resources of a multi-core processor efficiently.

___
## Generate archives

To generate archives go to the xml_archives folder and run the following command
```py
python generate_archives.py
```

___
## Make csv reports

To make csv reports go to the xml_archives folder and run the following command
```
python make_reports.py
```

___
## Tests

The program was tested on Python 3.10. No additional dependencies are required at this stage.

To run all tests go to the xml_archives folder and run the following command
```py
python -m unittest discover -v tests
```

___
## TODO
1. add more tests
2. add an implementation without multiprocessing
3. add an implementation with asyncio
4. add performance tests and compare all implementations
