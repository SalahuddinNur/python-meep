import subprocess
import re

def main(args):
    ivalue = float(args['T_Arc']['ivalue'])
    step = float(args['T_Arc']['step'])
    fvalue = float(args['T_Arc']['fvalue'])

    for i in range(0, int((fvalue-ivalue)/step) + 1):
        bendstrwo = 'bend' + '_' + str(ivalue + i * step) + '_woarc'
        bendstrw  = 'bend' + '_' + str(ivalue + i * step) + '_warc' 
        subprocess.call('mpirun -np 12 --allow-run-as-root /root/anaconda2/envs/pmp/bin/python ARC.py -n -v ' + str(ivalue + i * step) + ' | tee ' + bendstrwo + '.out', shell=True)
        subprocess.call('mpirun -np 12 --allow-run-as-root /root/anaconda2/envs/pmp/bin/python ARC.py -v ' + str(ivalue + i * step) + ' | tee ' + bendstrw + '.out', shell=True)
        subprocess.call('grep flux1: ' + bendstrwo + '.out > ' +  bendstrwo + '.dat', shell=True)
        subprocess.call('grep flux1: ' + bendstrw + '.out > ' + bendstrw + '.dat', shell=True)
        

def readArg():
    f = open('./arguments.txt', 'r')
    args = {}
    
    for line in f:
        res = re.split('[\s=:]+', line)
        arg = {}
        arg['ivalue'] = res[1]
        arg['step'] = res[2]
        arg['fvalue'] = res[3]
        args[res[0]] = arg
    return args


if __name__ == "__main__":
    args = readArg()
    main(args)

