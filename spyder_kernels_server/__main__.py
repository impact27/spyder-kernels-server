# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2009- Spyder Kernels Contributors
#
# Licensed under the terms of the MIT License
# (see spyder_kernels/__init__.py for details)
# -----------------------------------------------------------------------------
import sys
import zmq
import json
from spyder_kernels_server.kernel_server import KernelServer


def main(port):
    if len(sys.argv) > 1:
        port = sys.argv[1]

    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:%s" % port)
    print(f"Server running on port {port}")
    kernel_server = KernelServer()
    shutdown = False

    while not shutdown:
        #  Wait for next request from client
        message = socket.recv_pyobj()
        print(message)
        cmd = message[0]
        if cmd == "shutdown":
            shutdown = True
            kernel_server.shutdown()

        elif cmd == "open_kernel":
            try:
                cf = kernel_server.open_kernel(message[1])
                print(cf)
                with open(cf, "br") as f:
                    cf = (cf, json.load(f))

            except Exception as e:
                cf = ("error", e)
            socket.send_pyobj(["new_kernel", *cf])

        elif cmd == "close_kernel":
            kernel_server.close_kernel(message[1])


if __name__ == "__main__":
    port = "5556"
    main(port)
