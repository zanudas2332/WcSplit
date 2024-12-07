import codecs
import math
from idlelib.searchengine import get_line_col
from itertools import count

import click
import tqdm


@click.command()
@click.argument('filename')

@click.option(
    '--count', '-c', count = True,
    help = 'Count lines in file',
)
@click.option(
    '--lines', '-1',
    help = 'Lines number in cut parts of line'
)
@click.option(
    '-buffer', '-b',
    help = 'Lines number in cut parts of line'
)

def lines_counter(filename):
    line_count = 0
    for line in tqdm(read_file(filename), ascii = True, dynamic_ncols =True, total = line_count, unit = " lines"):
        line_count += 1
    return line_count

def read_file(filename):
    try:
        with codecs.open(filename, 'r', encoding= 'utf-8', errors= 'ignore') as file:
            for line in file:
                yield line
    except IOError:
        print("Can't read from file, IO error")
        exit(1)

def write_file(filename, data):
    try:
        with codecs.open(filename, 'r', encoding= 'utf-8', errors= 'ignore') as file:
            file.writelines(data)
        return True
    except IOError:
        print("Can't write to output")
        exit(1)

def lines_number_cut(filename, lines, buffer):
    lines_in_file, count_of_files, remain_lines = get_lines_cut_options(filename, lines)
    ranges_of_lines = get_ranges_of_lines(lines, count_of_files, remain_lines)
    print('File will cut on ' + str(count_of_files) + ' parts.')
    line_count = 1
    temp_1000_lines = []
    for line in tqdm(read_file(filename), ascii = True, dynamic_ncols = True, total = line_count, unit = " lines"):
        for key, value in ranges_of_lines.items():
            name = key + '.txt'
            start_line = value['start']
            end_line = value['end']
            if line_count >= start_line and line_count <= end_line:
                temp_1000_lines.append(line)
                if len(temp_1000_lines) > buffer:
                    write_file(name, temp_1000_lines)
                    del temp_1000_lines[:]
        line_count += 1


def get_lines_cut_options(filename, lines):
    lines_in_file = lines_counter(filename)
    count_of_files = math.ceil(lines_in_file / int(lines))
    remain_lines = lines_in_file % int(lines)
    return lines_in_file, count_of_files, remain_lines

def get_ranges_of_lines(lines, count_of_files, remain_lines):
    start_range = 1
    list_of_ranges = {}
    for current_file_number in range(count_of_files):
        if current_file_number <= count_of_files - 2:
            end_range = start_range + int(lines) - 1
        else:
            end_range = start_range + remain_lines
        lines_in_range = str(start_range) + '-' + str(end_range)
        list_of_ranges[lines_in_range] = {'start' : start_range, 'end': end_range}
        start_range = start_range + int(lines)
    return list_of_ranges



def main(filename, count, lines, buffer):          #### аргументы
    """
    A file tool that that can:
    - count lines in file,
    - cut file on parts with a given number of lines.
    """
    if filename is not None and count:
        print('Counting line in file: ', filename)
        lines_count = lines_counter(filename)
        print(f"In file {filename} {lines_count} lines")
    if filename is not None and lines is not None and buffer is not None:
        lines_number_cut(filename,lines,buffer)






if __name__ == "__main__":
    main()
