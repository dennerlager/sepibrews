import csv

class DsvDialect:
    """Dialect for Python's csv module.
    The format is as follows:
    field:field:field:field
    field:field:field:field
    Literal colons are escaped by backslash.
    Newlines in the data are also escaped by backslash.
    /etc/passwd is an example of a file that can be parsed with this dialect.
    Usage:
    import csv
    import dsv
    with open('a.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect=dsv.DsvDialect)
        writer.writerow(['Spam'] * 5 + ['Baked Beans'])
    with open('a.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, dialect=dsv.DsvDialect)
        for row in reader:
            print(row)
    """
    delimiter = ':'
    escapechar = '\\'
    quoting = csv.QUOTE_NONE
    lineterminator = '\n'
    skipinitialspace = False
    quotechar = ''
