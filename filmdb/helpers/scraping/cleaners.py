import re
import string
from datetime import datetime

regex = r"(\[|\()([^[(]+)(\]|\))"


def extract_year(title: str):
    min_year = 1900
    max_year = datetime.today().year

    matches = re.findall(regex, title)

    match_list = [to_int(match[1].strip()) for match in matches]

    years = filter(lambda x: x is not None and min_year <= x <= max_year, match_list)
    return next(years, None)


def clean_title(title: str):
    return re.sub(regex, "", title).strip(string.whitespace + "-")


def to_int(string: str):
    try:
        converted = int(string)
    except ValueError:
        converted = None
    return converted
