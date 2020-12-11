import csv
import re
import argparse

parser = argparse.ArgumentParser(description='Split grouped tags...')

parser.add_argument('tag_column_idx', type=int, help='number of the column to be split (starting with 1)')
parser.add_argument('filename', type=str, help='CSV file to be processed')
parser.add_argument('-s', dest='suffix', default='processed', help='filename suffix for the processed file')

args = parser.parse_args()

src_filename = args.filename
tag_column_idx = args.tag_column_idx
suffix = args.suffix

#######################

assert src_filename.endswith('.csv'), 'The input file format must be CSV!'

#######################

tag_column_idx = tag_column_idx - 1
out_filename = re.sub(r'\.csv$', '-' + suffix + '.csv', src_filename)

#######################

def flatten(arr):
  return [item for sublist in arr for item in sublist]

with open(src_filename) as csvfile:
  reader = csv.reader(csvfile, delimiter=',', quotechar='"')

  rows = list(reader)
  headers, rows = rows[0], rows[1:]

  tag_strs = flatten(list(map(
    lambda row: row[tag_column_idx].split(' '),
    rows
  )))
  tag_set = set(tag_strs)

  print(f'Found {len(tag_set)} tags')

  tag_list = list(tag_set)
  tag_list.sort()

  out_headers = headers + tag_list

  out_rows = list(
    map(
      lambda row: row + list(map(lambda tag: tag if (tag in row[tag_column_idx].split(" ")) else '', tag_list)),
      rows
    )
  )

  with open(out_filename, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(out_headers)
    for r in out_rows:
      writer.writerow(r)
