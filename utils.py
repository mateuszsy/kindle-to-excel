import psutil
from exceptions import PartitionExistsError


def validate_partition_name(arg_partition):
    partitions = psutil.disk_partitions()

    partition_exists = False
    for partition in partitions:
        partition_name = arg_partition + ':\\'
        if partition_name in partition and 'removable' in partition.opts:
            partition_exists = True

    if not partition_exists:
        raise PartitionExistsError(arg_partition)
