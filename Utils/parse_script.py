import re
import pandas as pd

pattern = r'([a-zA-z\s]+):(.+)'

data = {
  'name':[],
  'line':[]
}

nline = []

with open('script1.txt', 'r') as f:
  n = []
  for i in f:
    n.append(i.replace(';',''))

with open('script.txt', 'a') as f:
  for i in n:
    f.write(f'{i}\n')
