from datetime import datetime

from tools import downloader
from tools.utils import parse_str_to_date


def setup(date):
    # Check if date is passed as argument, set to default (today) otherwise
    if date is None:
        date = datetime.now()
    else:
        date = parse_str_to_date(date)
    print(date)


if __name__ == '__main__':

