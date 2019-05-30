import subprocess
import sys

def install():
    subprocess.call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


    
if __name__ == '__main__':
    install()
