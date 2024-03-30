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
    header_bytes = set()  # ex '00001010' -> the dictionary, set of distinct bytes present in file
    header_len = 0  # ex: '000000011' -> length of dictionary
    dictionary_sorted = dict()
    compressed_dict_value_length = 0
    mapper = dict()  # create mapper (chars -> compressed chars), ex. mapper['A'] = '00'
    compressed_file_length = 0
    num_added_bits_dec = 0  # (0-7) how many bits to add at the end of the file
    added_bits = ''  # ex '010'
    end_bits = ''  # ex '00'

    # get file statistics
    with open(input_file_name, 'rb') as f:
        # get content from input file
        next_byte = f.read(1)
        while next_byte:
            compressed_file_length += 1  # increment file length in bytes
            header_bytes.update([next_byte[0].to_bytes(1, 'big')])
            next_byte = f.read(1)

        # sort dict (for consistency)
        dictionary_sorted = sorted(header_bytes)

        # set size of compressed dict char (bits)
        compressed_dict_value_length = math.ceil(math.log(len(header_bytes), 2))

        # convert compressed file length to bits  # 3 bits -> added_bits length
        compressed_file_length = 3 + (compressed_file_length * compressed_dict_value_length)

        # set info about added bits
        num_added_bits_dec = (8 - compressed_file_length) % 8
        added_bits = (bin(num_added_bits_dec)[2:]).zfill(3)
        end_bits = '0' * num_added_bits_dec

        i = 0
        for byte in dictionary_sorted:
            mapper[byte] = bin(i)[2:].zfill(compressed_dict_value_length)  # binary value ex. '001'
            i += 1
        del i

        header_len = len(header_bytes).to_bytes(1, 'big')

    # compress and save to file
    output_f = open(output_file_name, 'wb')
    with open(input_file_name, 'rb') as f:
        # write header and dict to output file
        output_f.write(header_len)  # write size of dict
        # write dict
        for byte in dictionary_sorted:
            output_f.write(byte)

        # get content from input file
        compressed_content = added_bits
        next_byte = f.read(1)
        while next_byte:
            compressed_content += mapper[next_byte]

            # read next byte
            next_byte = f.read(1)

            # if this is the last byte append end_bits
            if not next_byte:
                compressed_content += end_bits

            # write compressed content to file
            while len(compressed_content) >= 8:
                # print('0b' + compressed_content[i:i + 8])  # bin value
                # print(int('0b' + compressed_content[i:i+8], 2))  # dec value
                # print(hex(int('0b' + compressed_content[i:i + 8], 2)))  # hex value

                decimal = int(compressed_content[0:0 + 8], 2)  # convert 8 bits to binary value
                output_f.write(decimal.to_bytes(1, 'big'))  # write byte to file
                compressed_content = compressed_content[8:]

        # close output file
        output_f.close()

        # show details if specified
        if show_details:
            print('###################################')
            print('#           compression           #')
            print('###################################')
            print(f'compression mapper: {mapper}')
            print(f'header dict: {dictionary_sorted}')
            print(f'dict key length: {compressed_dict_value_length}')
            print(f'dict length: {len(header_bytes)}')
            print(f'num added bits: {num_added_bits_dec}')
            print(f'added bits (bin): {added_bits}')
            print(f'end bits (bin): {end_bits}')


def decompress(input_file_name, output_file_name):
    output_f = open(output_file_name, 'wb')
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

        compressed_content: str = bin(next_byte)[2 + 3:].zfill(5)  # first 5 bits of compressed data

        # read compressed file byte by byte
        next_byte = f.read(1)
        while next_byte:
            compressed_content += bin(next_byte[0])[2:].zfill(8)

            # read next byte
            next_byte = f.read(1)

            # write decompressed chars to output file
            while (len(compressed_content) >= compressed_dict_key_length)\
                    and (len(compressed_content) > num_added_bits_dec):
                output_f.write(mapper[compressed_content[0:0 + compressed_dict_key_length]])
                compressed_content = compressed_content[compressed_dict_key_length:]

        # close output file
        output_f.close()

        # show details if specified
        if show_details:
            print('###################################')
            print('#          decompression          #')
            print('###################################')
            with open(output_file_name, 'rb') as tmp:
                print(f'decompressed content (first 20 bytes): {tmp.read(20)}')
            print(f'decompression mapper: {mapper}')
            print(f'dict key length: {compressed_dict_key_length}')
            print(f'dict length: {header_value}')
            print(f'num added bits: {num_added_bits_dec}')


####################
# main program logic
if decompress_flag:
    decompress(input_file, output_file)
else:
    compress(input_file, output_file)

# FIXME: decompression test
# decompress(output_file, 'decompressed_file.txt')
