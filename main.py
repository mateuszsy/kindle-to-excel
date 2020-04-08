import argparse
import os

import utils

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Present Kindle vocab data in a spreadsheet.')
    parser.add_argument('-f', '--format',
                        action='store_true',
                        help='Extract readable Kindle data')
    parser.add_argument('-n', '--name',
                        type=str,
                        help='Spreadsheet file name',
                        default='kindle_vocab')
    parser.add_argument('-p', '--partition',
                        type=str,
                        help='Partition letter for kindle removable',
                        default='E')
    args = parser.parse_args()

    # Check if specified partition exists
    utils.validate_partition_name(args.partition)

    vocab_path = '{}:\\system\\vocabulary\\vocab.db'.format(args.partition)
    if not os.path.exists(vocab_path):
        raise FileExistsError
