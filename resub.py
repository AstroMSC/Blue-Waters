#!/usr/bin/python
import glob
import math
import os
import sys
import shutil as sh
from subprocess import Popen,PIPE
import time as tm

username = 'clement'

qstat = Popen('qstat -u ' + username, shell=True, stdout=PIPE).stdout
qstat =  qstat.read().count(username)
n_scratch = glob.glob('/u/eot/' + username + '/scratch/*')
if float(len(n_scratch)) != float(qstat):
    print str(int(float(len(n_scratch))-float(qstat)))+ ' things not running that should be running'

for gpujob in glob.glob('/u/eot/' + username + '/scratch/*/genga'):
    dir = gpujob.replace('/genga','')
    for donejob in glob.glob(dir + '*.bw.out'):
        os.remove(donejob)
        times = []
        for datf in glob.glob(dir + '/*0*.dat'):
            time = datf.replace(dir + '/','')
            time = float(time.replace('.dat','')[-12:])
            times.append(time)
        time_now = max(times)
        param = open(dir + '/param.dat','r').readlines()
        time_steps =float(param[2].split()[-1])
        time_stop = float(param[7].split()[-1])
        if time_now < time_stop-time_steps:
            os.chdir(dir)
            Popen('qsub run_genga', shell=True, stdin=PIPE).stdout
            tm.sleep(5)
            print 'GPU job running in ' + dir + ' timed out'
        else:
            print 'GPU job running in ' + dir + ' completed, moving to results folder'
            new_loc = dir.replace('scratch','results')
            sh.move(dir,new_loc)

for joblist in glob.glob('/u/eot/clement/scratch/*/joblist'):
    jobdir = joblist.replace('/joblist','')
    sp_job = jobdir.replace('/u/eot/' + username + '/scratch/','')
    os.chdir(jobdir)
    cpus = 0
    for done_job in glob.glob(sp_job + '.o*'):
        print 'Sims running in ' + sp_job + ' timed out'
        os.remove(done_job)
        cpus = float(len(open('joblist','r').readlines()))
         for param in glob.glob('*/param.dmp'):
            del_dir = 'n'
            big = param.replace('param','big')
            dir = param.replace('/param.dmp','')
            with open(big,'r') as f:
                d = f.readlines()
            t_now = float(d[4].split()[4])
            t_stop = open(param,'r').readlines()[7].split()[-1]
            if (t_now >= (.995*t_stop)):
                with open('joblist','r') as file:
                    jobs = file.readlines()
                for j in range(len(jobs)):
                    if dir + ' ' in jobs[j]:
                    del_dir = j
                if del_dir != 'n':
                    print 'Job completed in ' + sp_job + '/' + dir
                    del jobs[del_dir]
                    del del_dir
                    cpus = cpus - 1
                with open('joblist','w') as file:
                    file.writelines(jobs)
        with open('run','r') as f:
            d = f.readlines()
        nodes = str(int(math.ceil(float(cpus)/32.)))
        cpus = str(int(cpus))
        d[2] = '#PBS -l nodes=' + str(nodes) + ':ppn=32:xe\n'
        d[13] = 'aprun -n ' + str(cpus) + ' ./scheduler.x joblist /bin/bash > out.log\n'
        with open('run','w') as f:
            f.writelines(d)
        Popen('qsub run', shell=True, stdin=PIPE).stdout
        sys.exit(0)
