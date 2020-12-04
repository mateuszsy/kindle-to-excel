import xlsxwriter

from exceptions import PartitionNotFoundError
import psutil
import os


def _validate_partition_name(arg_partition):
    partitions = psutil.disk_partitions()

    for partition in partitions:
        partition_name = f'{arg_partition}:\\'
        if partition_name in partition and 'removable' in partition.opts:
            return True
    raise PartitionNotFoundError(arg_partition)


def find_file(partition, trailing_path):
    _validate_partition_name(partition)

    lookup_path = f'{partition}:\\{trailing_path}'
    if not os.path.exists(lookup_path):
        raise FileNotFoundError(lookup_path)
    return lookup_path


def build_excel_workbook(data, file_name, columns, worksheet_name='Default'):
    workbook = xlsxwriter.Workbook(f'{file_name}.xlsx')
    worksheet = workbook.add_worksheet(worksheet_name)

    for column, column_name in enumerate(columns):
        worksheet.write(0, column, column_name)

    for row, word in enumerate(data):
        col = 0
        for value in word:
            worksheet.write(row + 1, col, value)
            col += 1
    workbook.close()
