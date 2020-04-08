class PartitionExistsError(Exception):
    def __init__(self, *args):
        self.partition_name = args[0]

    def __str__(self):
        return '\'{}:\\\' partition not found'.format(self.partition_name)
