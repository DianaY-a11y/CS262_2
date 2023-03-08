# CS262 Project 2

## Instructions: 

1.	Open ONE terminal only
2.	Run python3 run.py
3.	This creates three virtual machines in the file itself and doesn't need user based parameters to get access

- **[id] refers to the machine id number**
- **[speed] refers to number of operations able to be executed in a minute**
- **[logical clock time] – [system time] refers to the parameters specified in the investigation**

4.	Shut down the program when finished

## Documentation: 

The code first initializes multiple virtual machines and will each have a logical clock at a clock rate determined randomly. For the clock ticks, it will pick a random number from 1 to 6 for each real world second and updates the logical clock accordingly. The initialization also involves connecting with other virtual machines, open files for the log, listen to other sockets, and have a network queue for the incoming messages. 

Our code will also start off with checking if there is a message in the queue. If there is none, then the machine will generate a random number from 1 to 10 where 1 sends a message to one of the machines with the local logical clock time, update its own, and update the log accordingly; if the number is 2, it sends to the other machine that is the local logical time, update its own clock and log, and if it’s three sends to both other machinese. If it’s none of the above, then there is no sending that takes place. If a machine then has the message in the queue, it will take one message off update the clock, and record down that it has received a message in the log. 

Finally, we will run the scale model at least five teams for at least one minute each and look at the different size of jumps in the logical clocks compared to the system time and how this is impacted by the different timings (by looking at message queues and logical clock gaps). The experimentation outline is mentioned below as well as the findings we have identified.  

## Experimentation Scope:

Experiment 1 has the default setting on randomizations for the clock ranging from 1 to 6 and for the machine ranging from 1-10. 

Experiment 2 has the default setting for the machine randomization but we reassigned a different constant on the clock randomization to narrow down the variation in the clock cycles. 

Experiment 3 has the default setting for the clock randomization but we removed the situation in which an internal event would occur. 

## Design Choices:

We have set the code up in a way where a given user can provide certain inputs that runs on different experiments (see the initialization side for what the parameters look like). We have utilized the creation of two sockets, one for receiving messages in one thread and the other for just sending.  By setting up this wire protocol and through a multi-threaded system, this ensures that there is no limbo zone where all the machines are waiting for a onnection without even starting the connection in the first place. Each new connection will also be started in a new thread and receive mssages there for the same reason. 







