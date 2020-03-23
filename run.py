import os 
import time

def runtests():
    os.system("winpty -Xallow-non-tty ~/Downloads/python-3.8.2-embed-amd64/Scripts/pytest.exe > log")
    os.system("sed 's/\\?//g' log > log.txt")
    os.system("sed 's/\\x1b\\[[0-9;]*[a-zA-Z]//g' log.txt > log2.txt")
    os.system("mv log2.txt log.txt")

every = 3600 * 3
while True:
    dt = time.time()
    runtests()
    dt = time.time() - dt
    time.sleep(every - dt)

