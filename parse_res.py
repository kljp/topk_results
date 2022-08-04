import argparse
import re

parser = argparse.ArgumentParser(description='Usage')
parser.add_argument('--job', required=True, help='The job number to parse')
args = parser.parse_args()
filename = './job/topk.e' + args.job

f = open(filename, 'r')

cnt_speed = 0;
speed = 0;

loss = []
acc = []

while True:
    line = f.readline()
    if not line: break
    if line.find('py:90'):
        m = re.search('Speed: (.*?) images', line)
        if m is not None:
            m2 = str(m.group(1))
            if not 'f' in m2:
                #print(float(m2))
                cnt_speed = cnt_speed + 1
                speed = speed + float(m2)
    if line.find('py:822'):
        ls = re.search('val loss: (.*?),', line)
        if ls is not None:
            loss.append(str(ls.group(1)))
        ac = re.search('top-1 acc: (.*?),', line)
        if ac is not None:
            acc.append(str(ac.group(1)))
        
#print(speed / cnt_speed)
#print(loss)
#print(acc)

f.close()

fn_speed = './speed/speed-' + args.job
with open(fn_speed, 'w') as f2:
    f2.write(str(speed / cnt_speed))

fn_loss = './loss/loss-' + args.job
with open(fn_loss, 'w') as f3:
    f3.write('\n'.join(loss))

fn_acc = './acc/acc-' + args.job
with open(fn_acc, 'w') as f4:
    f4.write('\n'.join(acc))
