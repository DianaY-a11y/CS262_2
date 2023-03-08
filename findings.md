Run the scale model at least 5 times for at least one minute each time. Examine the logs, and discuss (in the lab book) the size of the jumps in the values for the logical clocks, drift in the values of the local logical clocks in the different machines (you can get a god’s eye view because of the system time), and the impact different timings on such things as gaps in the logical clock values and length of the message queue. Observations and reflections about the model and the results of running the model are more than welcome.

## Experiment 1: Random Clock Rates
<img width="1475" alt="Screen Shot 2023-03-08 at 1 27 40 AM" src="https://user-images.githubusercontent.com/80307545/223648331-295eb678-2804-4e2f-ab78-0d7c823915f3.png">
<img width="1291" alt="Screen Shot 2023-03-08 at 1 24 24 AM" src="https://user-images.githubusercontent.com/80307545/223648334-2e1bed73-fe44-421e-b5e9-b0523647fc08.png">
<img width="1194" alt="Screen Shot 2023-03-08 at 1 20 11 AM" src="https://user-images.githubusercontent.com/80307545/223648335-9a901d47-60f3-4264-a398-59d3361fb84a.png">
<img width="1211" alt="Screen Shot 2023-03-08 at 1 16 05 AM" src="https://user-images.githubusercontent.com/80307545/223648336-92363e9c-e285-4bb3-9312-288b7b8ceb31.png">
<img width="1188" alt="Screen Shot 2023-03-08 at 1 12 28 AM" src="https://user-images.githubusercontent.com/80307545/223648337-c2d939f8-e009-4d8e-b76b-52b6db9e267a.png">


In this experiment, we randomized the clock of each machine and logged the internal clock rate along with the actual time progression (in seconds) of 3 machines. We repeated this experiment a total of 5 times.

### Jump Size

From the tests, you can see that machines with lower clock_rates are more likely to experience periodic jump values in their internal clock compared to machines with higher clock_rates. As we can see, when machines are set to a clock rate of 1, they produce much more dynamic jump values than machine with other rates. Vice versa, machines with a clock rate of 6 note smaller jump values. This is logical because more acitivities occur between operations for slower machines.

### Value Drift

We see the drift value increases over time as the internal events cause the clocks of the machines to drift apart. The larger the difference in clock cycles between the machines and the more frequent and significant the internal events, the greater the drift value will be.

### Message Queue Length

There's a large variation in message queue length for machines operating on different clock cycles. As expected, machines often have a much shorter message queue than machines operating at slower times. As we can note in the data, machines operating at a clock cycle of 1/6 often has a message queue of 0 or 1. However, a machine with a clock cycle of 1/1 would have a message queue that stores up to 20-30 messages.

## Experiment 2: Identical Clock Rates
<img width="1555" alt="Screen Shot 2023-03-08 at 1 37 27 AM" src="https://user-images.githubusercontent.com/80307545/223648298-8f257271-01b9-4904-a2a3-71ea549ca5f6.png">

Here, we ran 3 machines for 2 minutes for five separate times. Each time it ran with an identical clock cycle, which is 3.

### Jump Size

As we can see in the graph, each machine engaged in jump values in a largely similar fashion with slight variations. Compared to the prevoius experiment where clock rates were randomized, each machine operated similarly and the graphed lines overlap more. Similar to the conclusion above, clock rate is highly rated in jump values. If clock rates if each machine is the same, they clickly produce the same internal clock rate versus actual time.

### Drift Values

Here, as expected, all machines have a similar drift in value and all converge at the same point (when at x, all have f(x) if f() is the function plotting one of the lines).

### Message Queue Length

This reaffirms our previous understanding of machines speeds and message queues lengths. These machines operating at an identical cycle all maintain around 1-2. Since these machines operate at identical times, they generally have the same message queue length.

## Experiment 3:
<img width="1483" alt="Screen Shot 2023-03-08 at 1 56 19 AM" src="https://user-images.githubusercontent.com/80307545/223648276-e0a0c3e2-34cc-4e0c-9ea2-0bd3b88dd368.png">
 No Internal Events

For this experiment, we ran 3 machines 5 times. Previously, we used a randomized a number between (1,10) and if the value was not 1,2, or 3, the machine would "treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value". For this experiment, we removed internal events. Therefore, if previously there was a 6/10 probability of performing an internal event, now there is 0.

### Jump Size

Since there are no internal events, the the jump size would be based solely on the difference in clock cycles between the machines. Similar to experiment 1, as the speed or clock cycle of the machine increases, its jump size decreases. Specifically, the jump size for a message sent from one machine to another would be equal to the difference in the clock cycles of the two machines at the time the message is sent.

### Drift Value

The drift value here increased which makes sense because the faster machine "gains" time as time progresses. Especially without internal events, there's zero probability for the program to reconvene or reduce their drift value.

### Message Queue Length

The message queue length across the board increased dramatically as some machines held a mesasge queue of nearly 100 messages. Without internal events, machines operating at slower times are then receiving more and more messages from faster machines than in a situation where there were internal events.
