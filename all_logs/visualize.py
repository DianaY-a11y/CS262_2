
import sys
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta


def clean_1(log):
    df = pd.DataFrame(log)
    line = df['Time'][0].split(" ")[1].split("/")[0]
    base_time = datetime.strptime(line, "%H:%M:%S")
    print(base_time)
    graph = {'time': [], 'internal_clock_1': []}
    for row in df['Time']:
        row = row.split(" ")[1].split("/")
        time_to_convert = datetime.strptime(row[0], "%H:%M:%S")
        time_diff = time_to_convert - base_time
        time_diff_seconds = time_diff.total_seconds()
        time_integer = int(time_diff_seconds)
        graph['time'].append(time_integer)
        graph['internal_clock_1'].append(int(row[1]))
    return pd.DataFrame(graph)


def clean(log):
    df = pd.DataFrame(log)
    line = df['Time'][0].split("/")[0]
    base_time = datetime.strptime(line, "%H:%M:%S")
    print(base_time)
    graph = {'time': [], 'internal_clock_1': []}
    for row in df['Time']:
        row = row.split("/")
        time_to_convert = datetime.strptime(row[0], "%H:%M:%S")
        time_diff = time_to_convert - base_time
        time_diff_seconds = time_diff.total_seconds()
        time_integer = int(time_diff_seconds)
        graph['time'].append(time_integer)
        graph['internal_clock_1'].append(int(row[1]))
    return pd.DataFrame(graph)


def analyze():
    log1_df = pd.read_csv("process_1.csv")
    log2_df = pd.read_csv("process_2.csv")
    log3_df = pd.read_csv("process_3.csv")

    df = clean(log1_df)
    df_2 = clean(log2_df)
    df_3 = clean(log3_df)

    fig, ax = plt.subplots()

    # Plot multiple lines
    ax.plot(df['time'], df['internal_clock_1'],
            label='machine 1: clock_rate = 2')
    ax.plot(df_2['time'], df_2['internal_clock_1'],
            label='machine 2: clock_rate = 4')
    ax.plot(df_3['time'], df_3['internal_clock_1'],
            label='machine 3: clock_rate = 4')

    ax.set_xlabel('Time')
    ax.set_ylabel('Internal Clock')
    ax.legend()

    # Show the plot
    plt.show()


analyze()
