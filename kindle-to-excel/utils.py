from exceptions import PartitionNotFoundError
import psutil
import os


def _validate_partition_name(arg_partition):
    """
    Check if parition exists.
    :param arg_partition: parition name
    :return: True if partition exists
    :raises: PartitionNotFoundError on partition not found
    """
    partitions = psutil.disk_partitions()
    partition_exists = False

    for partition in partitions:
        partition_name = '{}:\\'.format(arg_partition)
        if partition_name in partition and 'removable' in partition.opts:
            partition_exists = True

    if not partition_exists:
        raise PartitionNotFoundError(arg_partition)


def find_file(partition):
    """
    Get path to kindle db file
    :param partition: partition to look for file on
    :return: file path
    :raises: FileNotFoundError on file not found
    """
    _validate_partition_name(partition)

    vocab_path = '{}:\\system\\vocabulary\\vocab.db'.format(partition)
    if not os.path.exists(vocab_path):
        raise FileNotFoundError
    return vocab_path
