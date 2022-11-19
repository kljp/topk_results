import argparse
import re

parser = argparse.ArgumentParser(description='Usage')
parser.add_argument('--job', required=True, help='The job number to parse')
args = parser.parse_args()
filename = './job/topk.e' + args.job 
filename2 = './job/topk.o' + args.job 

f = open(filename, 'r')
f2 = open(filename2, 'r')

cnt_speed = 0
speed = 0

loss = []
acc = []

cnt_prop = 0
prop = 0

while True:
    line = f.readline()
    if not line: break
    if line.find('py:90') != -1:
        m = re.search('Speed: (.*?) images', line)
        if m is not None:
            m2 = str(m.group(1))
            if not 'f' in m2:
                #print(float(m2))
                cnt_speed = cnt_speed + 1
                speed = speed + float(m2)
    if line.find('py:822') != -1:
        ls = re.search('val loss: (.*?),', line)
        if ls is not None:
            loss.append(str(ls.group(1)))
        ac = re.search('top-1 acc: (.*?),', line)
        if ac is not None:
            acc.append(str(ac.group(1)))
    if line.find('py:731') != -1:
        m = re.search('forward \((.*?)\)', line)
        n = re.search('backward \((.*?)\)', line)
        if m is not None and n is not None:
            m2 = str(m.group(1))
            n2 = str(n.group(1))
            cnt_prop = cnt_prop + 1
            prop = prop + float(m2) + float(n2)
  
cnt_comm = 0
comm = 0

while True:
    line = f2.readline()
    if not line: break
    if line.find('COMM=*.') != -1:
        m = re.search('COMM=(.*?)\n', line)
        if m is not None:
            m2 = str(m.group(1))
            if float(m2) > 0.0001 and float(m2) < 1.0:
                cnt_comm = cnt_comm + 1
                comm = comm + float(m2)

print('Speed = %f' % (speed / cnt_speed))
#print(loss)
#print(acc)
print('Time = %f' % (128.0 / (speed / cnt_speed)))
print('Prop = %f' % (prop / cnt_prop))
print('Comm = %f' % (comm / cnt_comm))
print(cnt_comm)
f.close()
f2.close()

fn_speed = './speed/speed-' + args.job
with open(fn_speed, 'w') as f2:
    f2.write(str(speed / cnt_speed))

fn_loss = './loss/loss-' + args.job
with open(fn_loss, 'w') as f3:
    f3.write('\n'.join(loss))

fn_acc = './acc/acc-' + args.job
with open(fn_acc, 'w') as f4:
    f4.write('\n'.join(acc))
