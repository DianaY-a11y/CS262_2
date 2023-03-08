import unittest
import sys
import os
import socket
import time
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from process import Machine



class MachineTest(unittest.TestCase):

    HOST = '127.0.0.1'
    PORT = 8000

    def receive_messages(self) -> None:

        while not self.receive_has_ended:
            try:
                conn, addr = self.receive_socket.accept()
                response = conn.recv(1024)
                self.queue.append(response.decode())
            except:
                pass

    def setUp(self) -> None:
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
        self.machine_one.connect_machines([(self.machine_two.host, self.machine_two.port)])
        self.machine_two.connect_machines([(self.machine_one.host, self.machine_one.port)])

        self.assertIn((self.machine_one.host, self.machine_one.port), self.machine_two.connections)
        self.assertIn((self.machine_two.host, self.machine_two.port), self.machine_one.connections)
    
    def test_log_message(self) -> None:
        
        test_message = "Test Log Message!"
        self.machine_one.log_message(test_message)
        self.machine_one.logging.seek(0)

        log_content = self.machine_one.logging.read()
        
        self.assertIn(test_message, log_content)

    def test_receive_messages(self) -> None:
        
        rec_message = "Received!"
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        test_socket.connect((self.machine_one.host, self.machine_one.port))
        test_socket.send(rec_message.encode()) 
        
        time.sleep(self.machine_one.clock_rate + 1)
        test_socket.close()
        self.assertEqual(len(self.machine_one.queue), 1)
        self.assertEqual(rec_message, self.machine_one.queue.pop(0))

    def test_send_messages(self) -> None:
        # self.machine_one.connect_machines([(self.machine_two.host, self.machine_two.port)])
        # self.machine_two.connect_machines([(self.machine_one.host, self.machine_one.port)])

        message = "Sent this message"
        self.machine_one.send_message(msg=message, address=(self.internal_host, self.internal_port))
        
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(message, self.queue.pop(0))


if __name__ == "__main__":
    unittest.main()