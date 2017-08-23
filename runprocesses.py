# -*- coding: utf-8 -*-
# python runprocesses.py
import subprocess

process1 = subprocess.Popen("python flaskserver.py")
process2 = subprocess.Popen("node papanode/testsub2.py")

input("Press Enter to continue...")
process1.terminate()
process2.terminate()