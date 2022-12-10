import sys
import os
import io

def printf(string, end="\n"):
	sys.stdout.write(string + end)

def inputf():
	return io.BytesIO(os.read(0, os.fstat(0).st_size)).readline.decode()