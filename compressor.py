import argparse
import math


# setup argument parser
parser = argparse.ArgumentParser(prog='compressor.py', description='Program for compressing and decompressing files')
parser.add_argument('-d', '--decompress', action='store_true',
                    help='Decompress data in input_file and save it to output_file')
parser.add_argument('--details', action='store_true',
                    help="Print detailed information about compression / decompression")
parser.add_argument('input_file')
parser.add_argument('output_file')

# get parsed args
args = parser.parse_args()

decompress_flag = args.decompress
show_details = args.details
input_file = args.input_file
output_file = args.output_file

# FIXME: data used for testing
# decompress_flag = False
# show_details = True
# input_file = 'test_data.txt'
# output_file = 'compressed_file.txt'


# define functions for compression and decompression
def compress(input_file_name, output_file_name):
    with open(input_file_name, 'r', encoding='cp1252') as f:
        # get content from input file
        file_lines = f.readlines()
        file_lines = [line for line in file_lines]

        # get the set of distinct characters present in file
        dictionary = set()
        for line in file_lines:
            dictionary.update([char for char in line])

        # sort dict (for consistency)
        dictionary_sorted = sorted(dictionary)

        # get the string of distinct characters in file
        dictionary_str = ''.join(dictionary_sorted)

        #########
        # config
        compressed_dict_value_length = math.ceil(math.log(len(dictionary), 2))

        # create mapper (chars -> compressed chars), ex. mapper['A'] = '00'
        mapper = dict()

        i = 0
        for char in dictionary_sorted:
            mapper[char] = bin(i)[2:].zfill(compressed_dict_value_length)  # binary value ex. '001'
            i += 1
        del i

        header_dict = bytes(dictionary_str, 'cp1252')  # ex b'ABCD' -> the dictionary
        header_len = len(header_dict).to_bytes(1, 'big')  # ex: '0b000000011' -> length of dictionary

        # compress text in file (except new line characters')
        compressed_content = ''
        for line in file_lines:
            for char in line:
                compressed_content += mapper[char]

        compressed_file_length_bits = len(compressed_content) + 3  # +3 -> added_bits length
        num_added_bits_dec = 8 - (compressed_file_length_bits % 8)  # (0-7) how many bits to add at the end of the file
        added_bits = (bin(num_added_bits_dec)[2:]).zfill(3)  # ex '010'
        end_bits = '0' * num_added_bits_dec

        # add added_bits and end_bits to compressed file content
        compressed_content = added_bits + compressed_content + end_bits

        # write compressed content to output file
        with open(output_file_name, 'wb') as output_f:
            output_f.write(header_len)  # write size of dict
            output_f.write(header_dict)  # write dict

            # write compressed file content
            for i in range(0, len(compressed_content), 8):
                # print('0b' + compressed_content[i:i + 8])  # bin value
                # print(int('0b' + compressed_content[i:i+8], 2))  # dec value
                # print(hex(int('0b' + compressed_content[i:i + 8], 2)))  # hex value

                # convert 8 bits to binary value
                decimal = int(compressed_content[i:i + 8], 2)
                output_f.write(decimal.to_bytes(1, 'big'))  # write bytes to file

        # show details if specified
        if show_details:
            print('###################################')
            print('#           compression           #')
            print('###################################')
            print(f'file content (first line): {file_lines[0].strip()}')
            print(f'compression mapper: {mapper}')
            print(f'header dict: {header_dict}')
            print(f'dict key length: {compressed_dict_value_length}')
            print(f'dict length: {len(header_dict)}')
            print(f'compressed content (first 20 bits): {compressed_content[:20]}...')
            print(f'compressed content length: {len(compressed_content)}')
            print(f'num added bits: {num_added_bits_dec}')
            print(f'added bits (bin): {added_bits}')
            print(f'end bits (bin): {end_bits}')


def decompress(input_file_name, output_file_name):
    with open(input_file_name, 'rb') as f:
        #########
        # config
        header_value = f.read(1)[0]  # num of elements in dictionary
        compressed_dict_key_length = math.ceil(math.log(header_value, 2))

        # create mapper (compressed chars -> chars)
        mapper = dict()
        for i in range(header_value):
            mapper[bin(i)[2:].zfill(compressed_dict_key_length)] = f.read(1)

        next_byte = f.read(1)[0]
        num_added_bits_dec = next_byte >> 5  # first 3 bits

        compressed_content: str = bin(next_byte)[2:].zfill(8)  # first byte of compressed file
        bytes_to_decompress = f.read(-1)
        for byte in bytes_to_decompress:
            compressed_content += bin(byte)[2:].zfill(8)

        # write decompressed chars to output file
        with open(output_file_name, 'wb') as output_f:
            for i in range(3, len(compressed_content) - num_added_bits_dec, compressed_dict_key_length):
                output_f.write(mapper[compressed_content[i:i+compressed_dict_key_length]])

        # show details if specified
        if show_details:
            print('###################################')
            print('#          decompression          #')
            print('###################################')
            with open(output_file_name, 'r') as tmp:
                print(f'decompressed content (first line): {tmp.readline().strip()}')
            print(f'decompression mapper: {mapper}')
            print(f'dict key length: {compressed_dict_key_length}')
            print(f'dict length: {header_value}')
            print(f'content to decompress (first 20 bits): {compressed_content[:20]}...')
            print(f'content to decompress length: {len(compressed_content)}')
            print(f'num added bits: {num_added_bits_dec}')


####################
# main program logic
if decompress_flag:
    decompress(input_file, output_file)
else:
    compress(input_file, output_file)


# FIXME: decompression test
# decompress(output_file, 'decompressed_file.txt')
