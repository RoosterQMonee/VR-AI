from subprocess import run
from ctypes import cdll
import os

def clear_files(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))

def make(path, cppfile, ofile):
    run(
      ['g++',
       '-c',
       '-fPIC',
       f'{cppfile}',
       '-o',
       f'{path}/{ofile}']
    )

def compile_all(path, sofile, ofile):
    run(
      ['g++',
       '-shared',
       f'-Wl,-soname,{path}/{sofile}',
       '-o',
       f'{path}/{sofile}',
       f'{path}/{ofile}']
    )

def import_library(lib):
    return cdll.LoadLibrary(lib)

def cmake(dir, filename):
  clear_files(dir)
  make(dir, f'{filename}.cpp', f'{filename}.o')
  compile_all(dir, f'{filename}.so', f'{filename}.o')

class obj(object):
    def __init__(self, lib):
        self.obj = lib.Foo_new()
        self.lib = lib
        
    def exc(self):
        self.lib.Foo_bar(self.obj)
