import argparse
import re

parser = argparse.ArgumentParser(description='Usage')
parser.add_argument('--job', required=True, help='The result number to parse')
args = parser.parse_args()

f = open(args.job, 'r')

sp = args.job.split('results2/')
origin = sp[1]

rank0 = []
rank1 = []
rank2 = []
rank3 = []

while True:
    line = f.readline()
    if not line: break
    if line.find('[RANK 0.0] Error norm') != -1:
        ran0 = re.search('tensor\((.*?), device', line)
        if ran0 is not None:
            rank0.append(str(ran0.group(1)))
    if line.find('[RANK 1.0] Error norm') != -1:
        ran1 = re.search('tensor\((.*?), device', line)
        if ran1 is not None:
            rank1.append(str(ran1.group(1)))
    if line.find('[RANK 2.0] Error norm') != -1:
        ran2 = re.search('tensor\((.*?), device', line)
        if ran2 is not None:
            rank2.append(str(ran2.group(1)))
    if line.find('[RANK 3.0] Error norm') != -1:
        ran3 = re.search('tensor\((.*?), device', line)
        if ran3 is not None:
            rank3.append(str(ran3.group(1)))

size_rank = []
size_rank.append(len(rank0))
size_rank.append(len(rank1))
size_rank.append(len(rank2))
size_rank.append(len(rank3))
size_max = max(size_rank)
error = []
for i in range(size_max):
    error.append(str((float(rank0[i]) + float(rank1[i]) + float(rank2[i]) + float(rank3[i])) / 4.0))

f.close()

fn_error = './parsed_results/error/error-' + origin
with open(fn_error, 'w') as f2:
    f2.write('\n'.join(error))
