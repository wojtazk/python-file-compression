import argparse


# setup argument parser
parser = argparse.ArgumentParser(prog='fileCompressor', description='The program compresses and decompresses files')
parser.add_argument('-d', '--decompress', action='store_true')
parser.add_argument('input_file')
parser.add_argument('output_file')

# get parsed args
# args = parser.parse_args()
#
# decompress_flag = args.decompress
# input_file = args.input_file
# output_file = args.output_file

# FIXME:
decompress_flag = False
input_file = 'data.txt'
output_file = 'output.2137'


# define functions for compression and decompression
def compress(input_file_name, output_file_name):
    output_f = open(output_file_name, 'wb')
    with open(input_file_name, encoding='utf') as f:
        # get content from input file
        file_lines = f.readlines()
        file_lines = [line.strip() for line in file_lines]  # strip \n

        # FIXME:
        print(file_lines)

        # get the set of distinct characters present in file
        dictionary = set()
        for line in file_lines:
            dictionary.update([char for char in line])

        # get the string of distinct characters in file
        dictionary_str = ''.join(dictionary)

        # FIXME:
        print(dictionary)
        print(dictionary_str)

        #########
        # config
        compressed_dict_key_length = len(bin(len(dictionary))[2:])  # length in bits

        # create mapper

        header = len(dictionary).to_bytes(1, 'big')  # ex: '0b000000011' -> length of dictionary
        header_dict = bytes(dictionary_str, 'utf-8')  # ex b'ABCD' -> the dictionary

        file_bits_length = (sum([len(line) for line in file_lines]) * 8) + 3  # +3 -> added_bits length
        num_added_bits = 8 - (file_bits_length % 8)  # (0-7) how many bits were added at the end of the file
        num_added_bits = '0b' + "{:0>3}".format(bin(num_added_bits)[2:])  # ex '0b000'

        # FIXME:
        print(compressed_dict_key_length)
        print(header)
        print(header_dict)
        print(num_added_bits)

    output_f.close()


def decompress(input_file_name, output_file_name):
    output_f = open(output_file_name, 'w')
    with open(input_file_name, 'rb') as f:
        pass
    output_f.close()


####################
# main program logic
if decompress_flag:
    decompress(input_file, output_file)
else:
    compress(input_file, output_file)
