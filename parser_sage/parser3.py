import argparse
import re

parser = argparse.ArgumentParser(description='Usage')
parser.add_argument('--job', required=True, help='The result number to parse')
args = parser.parse_args()

f = open(args.job, 'r')

sp = args.job.split('parsed_results/denact/denact-')
origin = sp[1]

denepo = []

cnt = 0
acc = 0.0

while True:
    line = f.readline()
    if not line: break
    cnt = cnt + 1
    acc = acc + float(line)
    if cnt % 94 == 0:
        acc = acc / 94.0
        denepo.append(str(acc))
        acc = 0.0

f.close()

fn_denepo = './parsed_results/denepo/denepo-' + origin
with open(fn_denepo, 'w') as f2:
    f2.write('\n'.join(denepo))
