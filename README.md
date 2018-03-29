# Blue-Waters
Codes which manage simulations running remotely on Blue Waters

job_mange.sh runs on your local machine.  You must first set up ssh Control_master auto in your ~/.ssh/config file.
This way once you login with your password+pin the connection is maintained and job_manage.sh can ssh in to Blue Waters
on its own to restart sims.  An example config file is provided.

This manges Mercury (Chambers, 2001) and GENGA (Grimm et al 2014) simulations.

Steps:
1) Place the file config in ~/.ssh and change your username.
2) login to bluewaters and place resub.py in your home directory.
3) Make sure all Mercury simulations are 2 subdirectories deep in your scratch directory.
  a) Mercury simulations should be managed using scheduler.x (https://github.com/ncsa/Scheduler)
4) Make sure all Genga simulations are in there own directory in scratch.
5) Run ./job_manage.sh on your local machine at let it do all the work for you!
