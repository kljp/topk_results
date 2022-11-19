import argparse
import re

parser = argparse.ArgumentParser(description='Usage')
parser.add_argument('--job', required=True, help='The result number to parse')
args = parser.parse_args()

f = open(args.job, 'r')

sp = args.job.split('results/')
origin = sp[1]

job = origin.split('_')
task = job[0]
reducer = job[2]

accuracys = []
if reducer == 'sage':
    alphas = []
    betas = []
    gammas = []
    deltas = []
if reducer == 'sage' or reducer == 'thresh':
    denacts = []
    denavgs = []
bits = []

while True:
    line = f.readline()
    if not line: break
    if task == 'ncf':
        if line.find('best_accuracy') != -1:
            accuracy = re.search('best_accuracy\': (.*?), \'best', line)
            if accuracy is not None:
                str_acc = str(accuracy.group(1))
                epoch = re.search('best_epoch\': (.*?), \'best', line)
                if epoch is not None:
                    str_epo = str(epoch.group(1))
                    accuracys.append(str_epo + ' ' + str_acc)
    elif task == 'lstm':
        if line.find('last_perplexity') != -1:
            if line.find('split:test') != -1:
                accuracy = re.search('value:(.*?) \(split:test\)', line)
                if accuracy is not None:
                    accuracys.append(str(accuracy.group(1)))
    else:
        if line.find('last_accuracy') != -1:
            if line.find('split:test') != -1:
                accuracy = re.search('value:  (.*?) \(split:test\)', line)
                if accuracy is not None:
                    accuracys.append(str(accuracy.group(1)))
    if line.find('[Rank 0]') != -1 and line.find('[Iteration') != -1:
        if reducer == 'sage':
            alpha = re.search('a = (.*?), b', line)
            if alpha is not None:
                alphas.append(str(alpha.group(1)))
            beta = re.search('b = (.*?), c', line)
            if beta is not None:
                betas.append(str(beta.group(1)))
            gamma = re.search('c = (.*?), delta', line)
            if gamma is not None:
                gammas.append(str(gamma.group(1)))
            delta = re.search('delta = (.*?), e', line)
            if delta is not None:
                deltas.append(str(delta.group(1)))
        if reducer == 'sage' or reducer == 'thresh':
            denact = re.search('d = (.*?), m', line)
            if denact is not None:
                denacts.append(str(denact.group(1)))
            denavg = re.search('m = (.*?), bits', line)
            if denavg is not None:
                denavgs.append(str(denavg.group(1)))
        bit = re.search('bits = (.*?)\n', line)
        if bit is not None:
            bits.append(str(bit.group(1)))

f.close()

fn_accuracy = './parsed_results/accuracy/accuracy-' + origin
with open(fn_accuracy, 'w') as f2:
    f2.write('\n'.join(accuracys))

if reducer == 'sage':
    fn_alpha = './parsed_results/alpha/alpha-' + origin
    with open(fn_alpha, 'w') as f3:
        f3.write('\n'.join(alphas))
    fn_beta = './parsed_results/beta/beta-' + origin
    with open(fn_beta, 'w') as f4:
        f4.write('\n'.join(betas))
    fn_gamma = './parsed_results/gamma/gamma-' + origin
    with open(fn_gamma, 'w') as f5:
        f5.write('\n'.join(gammas))
    fn_delta = './parsed_results/delta/delta-' + origin
    with open(fn_delta, 'w') as f6:
        f6.write('\n'.join(deltas))

if reducer == 'sage' or reducer == 'thresh':
    fn_denact = './parsed_results/denact/denact-' + origin
    with open(fn_denact, 'w') as f7:
        f7.write('\n'.join(denacts))
    fn_denavg = './parsed_results/denavg/denavg-' + origin
    with open(fn_denavg, 'w') as f8:
        f8.write('\n'.join(denavgs))

fn_bit = './parsed_results/bit/bit-' + origin
with open(fn_bit, 'w') as f9:
    f9.write('\n'.join(bits))
