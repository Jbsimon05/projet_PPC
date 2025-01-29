import multiprocessing

from normal_traffic_gen import normal_traffic
from priority_traffic_gen import priority_traffic
from lights import lights_manager
from coordinator import coordinator

HIGH_PRIORITY_SIGNAL = multiprocessing.Event()
TRAFFIC_LIGHTS = multiprocessing.Array('i', [1, 1, 0, 0])

QUEUE_NORTH = multiprocessing.Queue()
QUEUE_SOUTH = multiprocessing.Queue()
QUEUE_EAST = multiprocessing.Queue()
QUEUE_WEST = multiprocessing.Queue()

normal_traffic = multiprocessing.Process(target=normal_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST))
priority_traffic = multiprocessing.Process(target=priority_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, HIGH_PRIORITY_SIGNAL))
lights = multiprocessing.Process(target=lights_manager, args=(TRAFFIC_LIGHTS, HIGH_PRIORITY_SIGNAL))
coordinator_process = multiprocessing.Process(target=coordinator, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, TRAFFIC_LIGHTS))

normal_traffic.start()
priority_traffic.start()
lights.start()
coordinator_process.start()