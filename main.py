import argparse
import os
from datetime import datetime

from config import *


def backup(db):
    filename = os.path.join(TMP_DIR, '{}{}-{}.sql'.format(FILENAME_PREFIX, db, datetime.now().strftime("%Y-%m-%d-%H-%M")))
    print('backup', db, 'to', filename)
    os.system('mysqldump -u {} {} > {}'.format(DB_USER, db, filename))
    parentid = None

    if db in GDRIVE_PARENTID:
        parentid = GDRIVE_PARENTID[db]

    if parentid:
        os.system('gdrive upload {} -p {}'.format(filename, parentid))
    else:
        os.system('gdrive upload {}'.format(filename))


def main():
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    parser = argparse.ArgumentParser()
    parser.add_argument('db', nargs='*')
    parser.add_argument('-e', '--exclude', action='append')
    parser.set_defaults(exclude=[])
    args = parser.parse_args()
    print(args)
    dblist = args.db
    if not dblist:
        dblist = DBLIST
    dblist = list(set(dblist) - set(args.exclude))
    print(dblist)
    for db in dblist:
        backup(db)


if __name__ == "__main__":
    main()
