import time
from hashlib import sha256
import random

#global settings
send_distance = 3 
channels = 16
number_of_users = 100
time_zones = 2
max_x = 10000
max_y = 10000
update_time = 20
send_package_range = 50
kill_package_range = 70
new_packet_likelines = 10

class anfranet:
    instances = []
    em_field = []
    sent_packets = {}

    def __init__(self, x = random.randint(0, max_x), y = random.randint(0, max_y), address = hex(random.randint(0,2**256)).replace("0x","")):
        anfranet.instances.append(self)
        self.x = x
        self.y = y
        self.addr = address
        self.my_queue = []
        self.net_function_queue = []
        self.active = true

    def update(cls):
        em_field = []
        for device in cls.instances:
            device.send()
        
        for device in cls.instances:
            device.determine_queues()



    def send(self, packet = ""):
        if self.active and len(self.my_queue) != 0 and len(packet) == 0:
            if self.my_queue[0] not in sent_packets:
                packet_number = len(sent_packets)
                sent_packets[self.my_queue[0]] = packet_number
            else:
                packet_number = sent_packets[self.my_queue[0]]
         my_queue.pop(0)
         em_field.append([self.x, self.y, packet_number])

        else:
            if self.active and len(self.my_queue) == 0 and len(self.net_function_queue) != 0 and len(packet) == 0:
                if self.net_function_queue[0] not in sent_packets:
                    packet_number = len(sent_packets)
                    sent_packets[self.net_function_queue[0]] = packet_number
                else:
                    packet_number = sent_packets[self.net_function_queue[0]]
        
            net_function_queue.pop(0)
            em_field.append([self.x, self.y, packet_number])
    
    def determine_queue(self):
        for place in em_field:
            if place[0] != self.x and place[1] != self.y and (self.x - place[0])**2 + (self.y - place[1])**2 <= send_distance:
                self.net_function_queue.append(sent_packets[place[3]])
            if random.randint(0,100) <= new_packet_likelines:
                self.my_queue.append(str())

device_a = anfranet(1,2)
device_b = anfranet(3,4)
print(device_b.addr)

