import sys
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_fwf('process_1.log')
df.to_csv('process_1.csv', index=None)
