def dump(flag: int, data_list: list):
    dump_data = []
    for data in data_list:
        if not isinstance(data, str):
            data = str(data)
        dump_data.append(data.replace(', ', R',\ '))
    return F'{flag};{', '.join(dump_data)}'


def parse_response(response: str):
    data_list = []
    flag, data_string = response.split(';')
    for data in data_string.split(', '):
        data_list.append(data.replace(R',\ ', ', '))
    return int(flag), data_list
