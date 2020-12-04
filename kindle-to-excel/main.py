import argparse
import re
import sqlite3
import utils


def parse_clippings(clipping):
    # Example line:
    # Wheel of Time [05]: The Fires of Heaven (Robert Jordan)
    book_author_regexp = r'(.*)\((.*?)\)'
    book_author_regexp_result = re.search(book_author_regexp, clipping[0])
    book, author = book_author_regexp_result.group(1), book_author_regexp_result.group(2)

    # Example line:
    # - Your Bookmark at location 11188 | Added on Friday, 31 May 2019 19:48:13
    clip_type_date_regex = r'.*?\s.*?\s(.*?) .*?, (.*?)$'
    clip_type_date_regex_result = re.search(clip_type_date_regex, clipping[1])
    clip_type, date = clip_type_date_regex_result.group(1), clip_type_date_regex_result.group(2)

    clipping = ' '.join(clipping[2:])

    return [book, author, clip_type, date, clipping]


def extract_clippings(clippings_path):
    clippings = []
    separator = '=========='
    with open(clippings_path, mode='r', encoding='utf-8-sig') as file:
        clipping_data = []
        for line in file:
            stripped_line = line.strip()
            if not stripped_line:
                continue

            if stripped_line == separator:
                clippings.append(clipping_data)
                clipping_data = []
            else:
                clipping_data.append(stripped_line)
    return clippings


def extract_vocab(vocab_path):
    conn = sqlite3.connect(vocab_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    sql_query = 'SELECT WORDS.word, WORDS.stem, LOOKUPS.usage, ' \
                'BOOK_INFO.title, BOOK_INFO.authors, WORDS.lang, LOOKUPS.timestamp ' \
                'FROM LOOKUPS ' \
                'LEFT JOIN BOOK_INFO ON LOOKUPS.book_key = BOOK_INFO.id ' \
                'LEFT JOIN WORDS ON LOOKUPS.word_key = WORDS.id;'
    rows = cur.execute(sql_query).fetchall()
    conn.close()

    return rows


def _main():
    vocab_path = utils.find_file(args.partition, 'system\\vocabulary\\vocab.db')
    clip_path = utils.find_file(args.partition, 'documents\\My Clippings.txt')

    if not args.no_vocab:
        vocab = extract_vocab(vocab_path)

        vocab_columns = ['word', 'stem', 'usage', 'title', 'authors', 'lang', 'timestamp']
        utils.build_excel_workbook(vocab, f'{args.name}_vocab', vocab_columns, 'Vocabulary')
    if not args.no_clip:
        clippings = map(parse_clippings, extract_clippings(clip_path))

        clippings_columns = ['book', 'author', 'type', 'date', 'clipping']
        utils.build_excel_workbook(clippings, f'{args.name}_clippings', clippings_columns, 'Clippings')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read Kindle vocab data to Excel spreadsheet.')
    parser.add_argument('-n', '--name',
                        type=str,
                        default='kindle',
                        help='Spreadsheet prefix to dump data to')
    parser.add_argument('-p', '--partition',
                        type=str,
                        default='E',
                        help='Partition for kindle removable')
    parser.add_argument('--no-vocab',
                        dest='no_vocab',
                        action='store_true',
                        help='Skip vocab file build')
    parser.add_argument('--no-clip',
                        dest='no_clip',
                        action='store_true',
                        help='Skip clippings file build')
    args = parser.parse_args()

    _main()
