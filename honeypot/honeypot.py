#!/usr/bin/env python3
"""Starter template for the honeypot assignment."""

import logging
import os
import time
import socket
from logger import create_logger

LOG_PATH = "/app/logs/honeypot.log"


def setup_logging():
    os.makedirs("/app/logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
    )


def run_honeypot():
    logger = create_logger(LOG_PATH)    
    logger.info("Honeypot starter template running.")
    ip = "0.0.0.0"
    port = 22
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(5)
    login_attemps = {}

    while True:
        
        client, addr = server.accept()
        logger.info(f"Connection found. IP: {addr[0]}:{addr[1]}")
        if addr[0] in login_attemps:
            login_attemps[addr[0]] += 1
            if login_attemps[addr[0]] > 3 :
                logger.info(f"Multiple connection attemps from {addr[0]}!")
        else:
            login_attemps[addr[0]] = 1
        time.sleep(.5)
        client.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")


if __name__ == "__main__":
    setup_logging()
    run_honeypot()
