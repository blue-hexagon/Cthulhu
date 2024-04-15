import random
from time import sleep

from src.passgen.distributor.payload_distributor import Client, ObjectTracker, SlidingWindowAction


def test_sliding_window_check():
    clients = [
        Client(ipv4_addr='127.0.0.1', port=8001),
        Client(ipv4_addr='127.0.0.1', port=8002),
        Client(ipv4_addr='127.0.0.1', port=8003),
    ]
    increment_threshold = ObjectTracker().INCREMENT_WHEN_SEEN_WITHIN_LAST_N_SECONDS
    decrement_threshold = ObjectTracker().DECREMENT_WHEN_SEEN_AT_LEAST_N_SECONDS_AGO
    for i in range(10):
        if i > increment_threshold:
            sleep(i)
            rand_client = clients[random.randint(0,len(clients)-1)]
            assert rand_client.tracker.get_sliding_window_action(hash(rand_client)) == SlidingWindowAction
