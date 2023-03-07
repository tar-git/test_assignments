"""Analyze the xmls archives and create two reports.

The following reports will be created:
1. levels.csv:   report on the levels of all xml files in all archives,
2. objects.csv:  report on the objects of all xml files in all archives.
"""

import shutil
from zipfile import ZipFile
import csv
from pathlib import Path
import xml.etree.ElementTree as ET
from contextlib import ExitStack
from multiprocessing import Pool, cpu_count
from itertools import chain

levels_path = 'reports/levels.csv'
objects_path = 'reports/objects.csv'


def write_to_report(data):
    """Write given data to the csv reports"""
    with ExitStack() as stack:
        levels = stack.enter_context(open(levels_path, 'w'))
        objects = stack.enter_context(open(objects_path, 'w'))
        levels_writer = csv.writer(levels)
        objects_writer = csv.writer(objects)
        for id_, level, objects in data:
            levels_writer.writerow((id_, level))
            objects_writer.writerows(zip([id_] * len(objects), objects))


def process_xml_file(xml_file_path: str | Path):
    """Extract payload from the given xml file"""
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    id_ = root[0].attrib['value']
    level = root[1].attrib['value']
    objects = [obj.attrib['name'] for obj in root[2]]
    return id_, level, objects


def process_xml_files(xml_files):
    """Make csv reports from all xml files concurrently"""
    with Pool(cpu_count()) as pool:
        async_results = [pool.apply_async(process_xml_file, (xf,))
                         for xf in xml_files]
        write_to_report([ar.get() for ar in async_results])


def get_xmls(zip_file_path: Path):
    """Extract all xml files from the given archive"""
    xml_path = zip_file_path.parent / zip_file_path.stem
    xml_path.mkdir(exist_ok=True)
    with ZipFile(zip_file_path, 'r') as zip_file:
        return [zip_file.extract(x, xml_path) for x in zip_file.namelist()]


def process_zip_files(zip_files_paths: list[Path]):
    """Extract all xml files from all archives concurrently"""
    with Pool(cpu_count()) as pool:
        async_results = [pool.apply_async(get_xmls, (zip_file_path,))
                         for zip_file_path in zip_files_paths]
        result = [ar.get() for ar in async_results]
        return chain(*result)


def cleanup(archives_paths: list[Path]):
    with Pool(cpu_count()) as pool:
        async_results = [
            pool.apply_async(shutil.rmtree, (path.parent / path.stem,))
            for path in archives_paths
        ]
        [ar.get() for ar in async_results]


def make_reports():
    """Entry point to make reports."""
    archives_path = Path('archives')
    reports_path = Path('reports')
    if not archives_path.exists():
        return
    if reports_path.exists():
        shutil.rmtree(reports_path)
    reports_path.mkdir()
    zip_files_paths = [f for f in archives_path.iterdir()
                       if f.suffix == '.zip']
    xml_files = process_zip_files(zip_files_paths)
    process_xml_files(xml_files)
    cleanup(zip_files_paths)


if __name__ == '__main__':
    make_reports()
