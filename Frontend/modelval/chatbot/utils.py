import json
import re


def extract_json_from_string(input_string):
    try:
        return json.loads(input_string)
    except ValueError:
        return json.loads(re.search(r"\s([{].*?[}])$", input_string).group(1))
