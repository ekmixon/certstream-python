import logging
import sys
import datetime
import certstream

def print_callback(message, context):
    logging.debug(f"Message -> {message}")

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        domain = "NULL" if len(all_domains) == 0 else all_domains[0]
        sys.stdout.write(
            f"""[{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}] {domain} (SAN: {", ".join(message['data']['leaf_cert']['all_domains'][1:])})\n"""
        )

        sys.stdout.flush()

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

certstream.listen_for_events(print_callback, url='wss://certstream.calidog.io/')