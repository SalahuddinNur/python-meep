import subprocess
import re

def main(args):
    ivalue = float(args['T_Arc']['ivalue'])
    step = float(args['T_Arc']['step'])
    fvalue = float(args['T_Arc']['fvalue'])

    for i in range(0, int((fvalue-ivalue)/step) + 1):
        bendstrwo = 'bend' + '_' + str(ivalue + i * step) + '_woarc'
        bendstrw  = 'bend' + '_' + str(ivalue + i * step) + '_warc' 
        
        #displayArgs ='/root/anaconda2/envs/mp/bin/python display.py ' + bendstrwo + '.dat ' + bendstrw + '.dat'
        subprocess.call('python display.py ' + bendstrwo + '.dat ' + bendstrw + '.dat', shell=True)


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

