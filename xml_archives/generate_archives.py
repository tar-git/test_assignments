"""Create "num_zips" zip archives with "num_xmls_in_zip" random xml files each.

See Readme.md for more details.
"""

__all__ = ('generate_archives', 'num_zips', 'num_xmls_in_zip')

import random
import string
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import uuid


num_zips = 50
num_xmls_in_zip = 100
max_objects_in_xml = 10
letters_and_digits = string.ascii_letters + string.digits
seen_random_strings = set()


def random_string(n: int):
    """Returns a random string of length n."""
    return ''.join(random.sample(letters_and_digits, n))


def create_xml_file(xml_file_path: str | Path):
    """Create a random xml file. See Readme.md for file structure."""
    root = ET.Element('root')
    ET.SubElement(root, 'var', {'name': 'id', 'value': uuid.uuid4().hex})
    ET.SubElement(root, 'var', {'name': 'level',
                                'value': str(random.randint(1, 100))})
    objects = ET.SubElement(root, 'objects')
    num_objects = random.randint(1, max_objects_in_xml)
    for _ in range(num_objects):
        random_str = random_string(random.randint(1, len(letters_and_digits)))
        ET.SubElement(objects, 'object', {'name': random_str})
    tree = ET.ElementTree(root)
    tree.write(xml_file_path)


def create_zip_file(zip_file_path: str | Path):
    """Create a zip archive with the "num_xmls_in_zip" number of xml files."""
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for i in range(num_xmls_in_zip):
            xml_file_name = f'file{i}.xml'
            xml_file_path = Path(zip_file_path).parent / xml_file_name
            create_xml_file(xml_file_path)
            zip_file.write(xml_file_path, xml_file_name)
            xml_file_path.unlink()


def generate_archives():
    """Entry point to create archives."""
    directory = Path('archives')
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir()
    for i in range(num_zips):
        zip_file_name = f'archive{i}.zip'
        zip_file_path = directory / zip_file_name
        create_zip_file(zip_file_path)


if __name__ == '__main__':
    generate_archives()
