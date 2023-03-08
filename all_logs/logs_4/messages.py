import sys
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

log_1 = pd.read_csv("process_1.csv")
log_2 = pd.read_csv("process_2.csv")
log_3 = pd.read_csv("process_3.csv")


def vis(log):
    df = pd.DataFrame(log)
    time = df['Time'][0].split('/')[0]
    base_time = datetime.strptime(time, "%H:%M:%S")
    graph = {'time': [], 'message_queue': []}
    for row in df['Time']:
        line = row.split("/")
        if len(line) == 4:
            graph['message_queue'].append(line[3][10:])
            time_to_convert = datetime.strptime(line[0], "%H:%M:%S")
            time_diff = time_to_convert - base_time
            time_diff_seconds = time_diff.total_seconds()
            time_integer = int(time_diff_seconds)
            graph['time'].append(time_integer)
    return pd.DataFrame(graph)


def vis_1(log):
    df = pd.DataFrame(log)
    time = df['Time'][0].split('/')[0][11:]
    base_time = datetime.strptime(time, "%H:%M:%S")
    graph = {'time': [], 'message_queue': []}
    for row in df['Time']:
        line = row.split("/")
        if len(line) == 4:
            graph['message_queue'].append(line[3][10:])
            time_to_convert = datetime.strptime(line[0][11:], "%H:%M:%S")
            time_diff = time_to_convert - base_time
            time_diff_seconds = time_diff.total_seconds()
            time_integer = int(time_diff_seconds)
            graph['time'].append(time_integer)
    return pd.DataFrame(graph)


df = vis_1(log_1)
df_2 = vis(log_2)
df_3 = vis_1(log_3)


fig, ax = plt.subplots()

# Plot multiple lines
ax.plot(df['time'], df['message_queue'],
        label='machine 1: clock_rate = 5')
ax.plot(df_2['time'], df_2['message_queue'],
        label='machine 2: clock_rate = 2')
ax.plot(df_3['time'], df_3['message_queue'],
        label='machine 3: clock_rate = 1')

ax.set_xlabel('Time')
ax.set_ylabel('Message Queue Length')
ax.legend()

# Show the plot
plt.show()
