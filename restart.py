import sys
import os

def restart_program(self):
    python = sys.executable
    os.execl(python, python, *sys.argv)