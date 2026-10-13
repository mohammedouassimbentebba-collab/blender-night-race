"""
Headless Blender MCP Server bridge.
Allows Blender to run headless while servicing MCP tool commands on localhost:9876.
"""
import sys
import time
import socket
import threading
import queue
import json
import traceback

try:
    import bpy
except ImportError:
    print("This script must be executed inside Blender via: blender --background --python headless_mcp_server.py", file=sys.stderr)
    sys.exit(1)

import blender_mcp

class HeadlessBlenderMCPServer(blender_mcp.BlenderMCPServer):
    def start_headless(self):
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        self.server_thread = threading.Thread(target=self._server_loop)
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f">>> Blender MCP Headless Server active and listening on {self.host}:{self.port} <<<", flush=True)

    def serve_forever(self):
        self.start_headless()
        try:
            while self.running:
                self._drain_command_queue()
                time.sleep(0.02)
        except KeyboardInterrupt:
            print("Stopping headless server...")
            self.stop()

if __name__ == "__main__":
    server = HeadlessBlenderMCPServer(host="localhost", port=9876)
    server.serve_forever()
