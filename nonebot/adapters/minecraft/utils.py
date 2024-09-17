def dump(flag: int, data_list: list):
    dump_data = []
    for data in data_list:
        if not isinstance(data, str):
            data = str(data)
        data = data.replace('\\', '\\\\')
        dump_data.append(data.replace(', ', ',\\ '))
    return F'{flag};{', '.join(dump_data)}'


def parse_response(response: str):
    data_list = []
    flag, data_string = response.split(';')
    for data in data_string.split(', '):
        data = data.replace(',\\ ', ', ')
        data_list.append(data.replace('\\\\', '\\'))
    return int(flag), data_list


if __name__ == '__main__':
    print(test := dump(1, input().split()))
    print(parse_response(test)[1][0])
