import unittest
import sys
import os
import socket
import time
import threading

# directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))
# parent directory
parent_dir = os.path.join(current_dir, '..')
# add parent directory to sys.path
sys.path.append(parent_dir)

from process import Machine



class MachineTest(unittest.TestCase):

    HOST = '127.0.0.1'
    PORT = 8000

    def receive_messages(self) -> None:
        """
        A function that receives messages on a socket and appends them to a queue concurrently until receive_has_ended is True.
        
        """

        while not self.receive_has_ended:
            try:
                conn, addr = self.receive_socket.accept()
                response = conn.recv(1024)
                self.queue.append(response.decode())
            except:
                pass

    def setUp(self) -> None:
        """
        A function that sets up the environment, i.e. required variables and objects for the test. 
        It creates instances of Machine class, sets up a socket to receive messages, and starts a thread for receiving messages concurrently.
        """
       
        self.log_file_one = 'machine_one_test.log'
        self.log_file_two = 'machine_two_test.log'
        self.buffer = 1

        self.receive_has_ended: bool = False
        self.internal_host: str = '127.0.0.1'
        self.internal_port: int = 6969
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_socket.bind((self.internal_host, self.internal_port))
        self.receive_socket.listen(5)
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        
        self.queue: list = []

        self.machine_one = Machine(id=1, host=MachineTest.HOST, port=MachineTest.PORT, log_file=self.log_file_one)
        MachineTest.PORT += 1
        self.machine_two = Machine(id=2, host=MachineTest.HOST, port=MachineTest.PORT, log_file=self.log_file_two)
        MachineTest.PORT += 1

    def tearDown(self) -> None:
        """
        A function that cleans up after the tests have been run.

        It deletes the log files created during the tests, stops the thread that receives messages, and shuts
        down the instances of the Machine class.
        """
        if os.path.exists(self.machine_one.log_file):
            os.remove(self.machine_one.log_file)
        
        if os.path.exists(self.machine_two.log_file):
            os.remove(self.machine_two.log_file)

        self.receive_has_ended = True
        self.receive_socket.close()
        self.receive_thread.join()

        print(self.machine_one.log_file)
        self.machine_one.shutdown()
        self.machine_two.shutdown()
        

    def test_connect_machines(self) -> None:
        """
        A test function that checks if the machines can connect to each other.

        This function checks if the machines can establish a connection to each other by calling the connect_machines()
        method of the Machine class and checking if the connections are established.
        """
        self.machine_one.connect_machines([(self.machine_two.host, self.machine_two.port)])
        self.machine_two.connect_machines([(self.machine_one.host, self.machine_one.port)])

        self.assertIn((self.machine_one.host, self.machine_one.port), self.machine_two.connections)
        self.assertIn((self.machine_two.host, self.machine_two.port), self.machine_one.connections)
    
    def test_log_message(self) -> None:
        
        """
        This function that checks if the log messages are written to the log file.

        It checks if the messages logged by the machine are written to the log file by calling the
        log_message() method of the Machine class and reading the contents of the log file
        
        """
        
        test_message = "Test Log Message!"
        self.machine_one.log_message(test_message)
        self.machine_one.logging.seek(0)

        log_content = self.machine_one.logging.read()
        
        self.assertIn(test_message, log_content)

    def test_receive_messages(self) -> None:
        
        """
        Test the receive_messages method of a machine object.
        Sends a message to the machine_one object and verifies that the message is received 
        and added to the machine_one queue correctly.
        """
        
        rec_message = "Received!"
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        test_socket.connect((self.machine_one.host, self.machine_one.port))
        test_socket.send(rec_message.encode()) 
        
        time.sleep(self.machine_one.clock_rate + 1)
        test_socket.close()
        self.assertEqual(len(self.machine_one.queue), 1)
        self.assertEqual(rec_message, self.machine_one.queue.pop(0))

    def test_send_messages(self) -> None:
        
        """
        Tests the send_message method of the Machine class by sending a message to a connected machine and 
        checking if the message is sent correctly and added to the target machine's message queue.

         """
        
        # self.machine_one.connect_machines([(self.machine_two.host, self.machine_two.port)])
        # self.machine_two.connect_machines([(self.machine_one.host, self.machine_one.port)])

        message = "Sent this message"
        self.machine_one.send_message(msg=message, address=(self.internal_host, self.internal_port))
        
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(message, self.queue.pop(0))


if __name__ == "__main__":
    unittest.main()
