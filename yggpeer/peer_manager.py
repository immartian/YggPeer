import socket
import threading
import time
import psutil

class PeerManager:
    def __init__(self, local_port=12345, discovery_port=10799):            

        # Check if the Yggdrasil interface is up
        if not self.is_yggdrasil_interface_up():
            raise Exception("Yggdrasil interface ygg0 is not up!")
        
        self.peers = {}  # Dictionary to store peer status and metadata
        self.local_port = local_port
        self.status_port = discovery_port
        self.lock = threading.Lock()  # To prevent race conditions when updating peer status
        self.continue_chat = True  # Control the continuous chat loop
        self.message_callback = None  # Placeholder for message callback function
    

    def is_yggdrasil_interface_up(self):
        """Dynamically check if an interface has an IPv6 address that matches Yggdrasil's pattern."""
        import re
        import ipaddress

        # valid Yggdrasil address starts with 2xx or 3xx, and it's ipvg
        pattern = r'^(2[0-9a-fA-F]{2}|3[0-9a-fA-F]{2})$'
        interfaces = psutil.net_if_addrs()

        for interface_name, addresses in interfaces.items():
            for addr in addresses:
                # validate the address start with reygg pattern
                if addr.family == socket.AF_INET6:
                    #ip = ipaddress.IPv6Address(addr.address).exploded
                    first_hex = addr.address.split(":")[0]
                    if re.match(pattern, first_hex):
                        print(f"Yggdrasil interface {interface_name} is up with address {addr.address}")
                        return True
        print("Yggdrasil interface is not found!")
        return False
    
    def add_peer(self, peer_ip, chat_port):
        """Add a new peer to the manager."""
        with self.lock:
            self.peers[peer_ip] = {
                'chat_port': chat_port,
                'status': 'unknown'
            }
    
    def update_peer_status(self, peer_ip, status):
        """Update the status of a peer."""
        with self.lock:
            if peer_ip in self.peers:
                self.peers[peer_ip]['status'] = status
                #print(f"Updated status for {peer_ip} to {status}")
    
    def get_peer_status(self, peer_ip):
        """Get the status of a peer."""
        with self.lock:
            return self.peers.get(peer_ip, {}).get('status', 'unknown')

    def broadcast_status_updates(self):
        """Periodically broadcast status updates to all peers."""
        while True:
            for peer_ip in list(self.peers):
                #print(f"Broadcast status check: {peer_ip} is available")
                pass
            time.sleep(5)  # Status update interval
    
    def start_status_server(self):
        """Start the server to respond to status requests from other peers."""
        status_server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        status_server.bind(('::', self.status_port))
        print(f"Status server is listening on port {self.status_port}...")
        
        while True:
            data, addr = status_server.recvfrom(1024)
            print(f"Received status request from {addr}")
            if data.decode('utf-8') == 'status':
                status = 'available'  # For now, always available. Can be dynamic.
                status_server.sendto(status.encode('utf-8'), addr)

    def send_message(self, peer_ip, message):
        """Send a message to a peer."""
        peer_data = self.peers.get(peer_ip)
        chat_port = peer_data['chat_port']
        client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        try:
            #print(f"Trying to connect to {peer_ip}:{chat_port}")
            client.connect((peer_ip, chat_port))
            client.send(message.encode('utf-8'))
            #print(f"Message sent to {peer_ip}")
        except socket.error as e:
            print(f"Error sending message to {peer_ip}: {e}")
        finally:
            client.close()

    def start_chat_server(self):
        """Start the chat server to handle incoming messages."""
        server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('::', self.local_port))
        server.listen(5)
        print(f"Chat server is listening on port {self.local_port}...")
        
        while True:
            conn, addr = server.accept()
            #print(f"Connected by {addr}")
            threading.Thread(target=self.handle_incoming_message, args=(conn, addr)).start()

    def handle_incoming_message(self, conn, addr):
        """Handle incoming messages and keep peer available after disconnection."""
        peer_ip = addr[0]  # Extract peer IP
        while True:
            try:
                message = conn.recv(1024).decode('utf-8')
                if not message:
                    #print("Connection closed.")
                    break
                #print(f"Received message: {message}")
                
                # If there's a callback, invoke it with the received message
                if self.message_callback:
                    self.message_callback(peer_ip, message)
            except socket.error as e:
                print(f"Error receiving message: {e}")
                break
        
        conn.close()
        
        # After the connection closes, set peer status back to available
        self.update_peer_status(peer_ip, 'available')

    def set_message_callback(self, callback):
        """Set the callback function to handle incoming messages."""
        self.message_callback = callback

    def start(self):
        """Start the Peer Manager's background services."""
        # Start the status server and chat server
        threading.Thread(target=self.start_status_server, daemon=True).start()
        threading.Thread(target=self.start_chat_server, daemon=True).start()

        # Broadcast status updates in the background
        threading.Thread(target=self.broadcast_status_updates, daemon=True).start()
