import socket
import os
import threading
import time
import sys
import random
import json

EVENTS = {
    "MACHINE_ONE": 1,
    "MACHINE_TWO": 2,
    "BROADCAST": 3,
    "INTERNAL_EVENT": 4,
}

class Machine:
    def __init__(self,
                id: int = 0,
                host: str = "127.0.0.1",
                port: int = 8000,
                clock_rate: int = None,
                clock_range_size: int = 6,
                log_file: str = None,
                ) -> None:
        
        """
        Constructor for generating a Machine Object. Default parameters are a process id,
        host, port, clock_rate, clock_range_size, and log_file
        """
        
        self.pid = id
        self.host = host
        self.port = port
        self.clock_rate = clock_rate
        self.clock_range_size = clock_range_size
        self.log_file = log_file
        self.logging = None
        self.logger_open: bool = False
        self.connections: list = []
        self.main_has_ended: bool = False
        self.receive_has_ended: bool = False
        self.set_clock()
        self.set_log_file()
        self.set_socket()

    def set_clock(self) -> None:
        """
        Initializes a clock rate and logical clock for the Machine
        """

        # Set clock tick to be reciprocal of clock_rate
        if not self.clock_rate:
            self.clock_rate = 1 / random.randint(1, self.clock_range_size)

        else: self.clock_rate = 1 / self.clock_rate

        self.local_clock = 0

    def set_log_file(self) -> None:
        """
        Initializes a log_file if not provided and createa an I/O Wrapper for the log_file
        """
        self.logger_open = True
        if not self.log_file:
            self.log_file = f"./logs/process_{self.pid}.log"
        else: self.log_file = "./logs/" + self.log_file

        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logging = open(self.log_file, 'a+')

    def receive_messages(self) -> None:
        """
        Receive Messages from other Machines on a socket
        """
        while not self.receive_has_ended:
            try:
                conn, addr = self.receive_socket.accept()
                response = conn.recv(1024)
                self.queue.append(response.decode())
            except:
                pass
    
    def set_socket(self) -> None:
        """
        Initializes a receive socket, and runs the receive_messages function in 
        its own thread so that events can still be generated in the main thread.
        """
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.bind((self.host, self.port))
        self.receive_socket.listen(5)

        self.queue: list = []
        # Spinup receive in its own thread
        self.main_receive_thread = threading.Thread(target=self.receive_messages)
        self.main_receive_thread.start()
    
    def connect_machines(self, connections: list = []) -> None:
        self.connections += connections

    def send_message(self, msg: str = "", address: tuple = ()) -> None:

        """
        Sends a message to another machine as desired
        """
        
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.send_socket.connect(address) # Connect to other virtual machine

        self.send_socket.send(msg.encode())
        self.send_socket.close()

    def log_message(self, msg: str) -> None:
        """
        Logs a message to the log_file
        """

        # Check if log_file I/O is already closed
        if self.logging.closed:
            return

        # System time
        current_time = time.time()
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))

        # Log Message
        complete_message = f"{formatted_time}/{self.local_clock}/{msg}"
        
        self.logging.write(complete_message + '\n')
        

    def generate_event(self) -> None:
        """
        When the Machine queue is not empty, will generate a random event 
        EVENTS: MACHINE_ONE, MACHINE_TWO, BROADCAST, INTERNAL_EVENT
        Check EVENTS global dict at the top of the file
        """

        msg = json.dumps({"sender" : f"process_{self.pid}",
                   "local_time" : self.local_clock,
                })

        # Change this to change probality of an internal event
        # Generates a random int in the range of EVENT_SIZE
        EVENT_SIZE = 10
        event = random.randint(1, EVENT_SIZE)
        self_log = ""

        if event == EVENTS["MACHINE_ONE"]:
            self_log = f"Sent to machine_{event}"
            self.send_message(msg=msg, address=self.connections[event-1])

        elif event == EVENTS["MACHINE_TWO"]:
            self_log = f"Sent to machine_{event}"
            self.send_message(msg=msg, address=self.connections[event-1])

        elif event == EVENTS["BROADCAST"]:
            self_log = f"Broadcast to all machines"
            for i in range(len(self.connections)):
                self.send_message(msg=msg, address=self.connections[i])

        else:
            self_log = "Internal event"
            # The internal event time can be modified
            time.sleep(.1)
        
        self.log_message(self_log)
        time.sleep(self.clock_rate)
            
            
    def main(self) -> None:
        """
        Driver function that either receives a message or generates an event
        """
    
        while not self.main_has_ended:

            if self.queue:

                msg = json.loads(self.queue.pop(0))
                msg_time = msg['local_time']
                # Update logical clock based on logical clock of other Machine messages
                # This is to prevent misordering of processes running on slower virtual machines
                # Slower machine will show clock drift
                self.local_clock = max(self.local_clock, msg_time) + 1

                # Format receiving a message
                self.log_message(f"RecFrom:{msg['sender']}/QueueSize:{len(self.queue) + 1}")
                time.sleep(self.clock_rate)
                continue

            else:
                self.local_clock += 1
                self.generate_event()



    def shutdown(self) -> None:
        """
        CLose sockets, log_file I/O and end thread processes
        """
        
        self.receive_socket.close()
        self.main_has_ended = True
        self.receive_has_ended = True
        self.main_receive_thread.join()

        if self.logger_open:
            self.logging.close()
        
        print(f"Shutdown vm_{self.pid}")

        


        
        


            



        


    
    
        
    
