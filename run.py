import os
print(os.environ['HOME'])


cwd = os.getcwd()

haha = os.path.realpath('paper.csv')
print(cwd)
print(str(haha))


python -c 'import loopandvote1; loopandvote1.loopthis("0330extras.csv",6000)'