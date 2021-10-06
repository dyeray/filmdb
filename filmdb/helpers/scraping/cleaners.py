import re
import string
from datetime import datetime

from helpers import find_first

regex = r"(\[|\()([^[(]+)(\]|\))"


def extract_year(title: str):
    min_year = 1900
    max_year = datetime.today().year
    matches = re.findall(regex, title)
    match_list = [to_int(match[1].strip()) for match in matches]
    return find_first(match_list, lambda x: x is not None and min_year <= x <= max_year)


def clean_title(title: str):
    return re.sub(regex, "", title).strip(string.whitespace + "-")


def to_int(string_obj: str):
    try:
        converted = int(string_obj)
    except ValueError:
        converted = None
    return converted
