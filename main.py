# input_file = input('Enter file name: ')
input_file_name = 'data.txt'
output_file_name = 'output.txt'

# compression
with open(input_file_name, encoding='utf') as f:
    # get content from input file
    file_lines = f.readlines()
    file_lines = [line.strip() for line in file_lines]  # strip \n

    file_bytes_lenghth = sum([len(line) for line in file_lines])

    # FIXME:
    print(file_lines)
    print(file_bytes_lenghth)

    # get the set of distinct characters present in file
    dictionary = set()
    for line in file_lines:
        dictionary.update([char for char in line])

    # get the sorted dictionary of distinct characters in file
    dictionary = sorted(dictionary)
    dictionary_str = ''.join(dictionary)

    # FIXME:
    print(dictionary)
    print(dictionary_str)

    # config
    header = len(dictionary).to_bytes(1, 'big')  # ex: '0b000000011'
    header_dict = bytes(dictionary_str, 'utf-8')  # ex b'ABCD'
    added_bits = bin(len(dictionary))  # ex '0b000'

    # FIXME:
    print(header)
    print(header_dict)
    print(added_bits)


