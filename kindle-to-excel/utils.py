from src.exceptions import PartitionExistsError
import psutil
import os


def validate_partition_name(arg_partition):
    partitions = psutil.disk_partitions()
    partition_exists = False

    for partition in partitions:
        partition_name = '{}:\\'.format(arg_partition)
        if partition_name in partition and 'removable' in partition.opts:
            partition_exists = True

    if not partition_exists:
        raise PartitionExistsError(arg_partition)


def find_file(partition):
    vocab_path = '{}:\\system\\vocabulary\\vocab.db'.format(partition)
    if not os.path.exists(vocab_path):
        raise FileExistsError
    return vocab_path
