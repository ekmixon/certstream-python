import time
from collections import deque

import certstream

import logging

logger = logging.getLogger('stat_counter')

NUM_MINUTES = 1
INTERVAL = NUM_MINUTES * 60

def callback(message, context):
    if not context.get('edge'):
        context.edge = time.time() + INTERVAL
        context.counter = deque()
        context.heartbeats = deque()

    if message['message_type'] != "heartbeat":
        context.counter.append(message)
    else:
        context.heartbeats.append(message)

    if time.time() > context['edge']:
        logger.info(
            f"Edge has been broken, writing out. {len(context.counter)} results for the last {NUM_MINUTES} minute/s ({len(context.heartbeats)} heartbeats)"
        )


        with open('/tmp/out.csv', 'a') as f:
            f.write(f"{time.time()},{len(context['counter'])}\n")

        context.counter.clear()
        context.heartbeats.clear()
        context.edge = time.time() + INTERVAL

certstream.listen_for_events(callback, url='wss://certstream.calidog.io/', skip_heartbeats=False)