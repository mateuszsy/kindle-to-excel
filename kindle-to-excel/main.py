import xlsxwriter
import argparse
import sqlite3
import utils


def extract(database_path):
    conn = sqlite3.connect(database_path)
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


def build_excel_workbook(vocabulary, file_name):
    workbook = xlsxwriter.Workbook('{}.xlsx'.format(file_name))
    worksheet = workbook.add_worksheet('Vocabulary')

    column_names = ['word', 'stem', 'usage', 'title', 'authors', 'lang', 'timestamp']
    for column, column_name in enumerate(column_names):
        worksheet.write(0, column, column_name)

    for row, word in enumerate(vocabulary):
        col = 0
        for value in word:
            worksheet.write(row + 1, col, value)
            col += 1
    workbook.close()


def _main():
    vocab_path = utils.find_file(args.partition)

    extracted_vocab = extract(vocab_path)
    build_excel_workbook(extracted_vocab, args.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read Kindle vocab data to Excel spreadsheet.')
    parser.add_argument('-n', '--name',
                        type=str,
                        default='kindle_vocab',
                        help='Spreadsheet name to dump data to')
    parser.add_argument('-p', '--partition',
                        type=str,
                        default='E',
                        help='Partition for kindle removable')
    args = parser.parse_args()
    _main()
