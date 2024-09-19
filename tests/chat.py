from yggpeer.peer_manager import PeerManager
import time


# Example usage
if __name__ == "__main__":
    def message_handler(src, msg):
        """Example of how an external app can handle received messages."""
        print(f"\n{src}: {msg}")

    peer_manager = PeerManager()

    # Add peers manually (for now)
    peer_ip = "201:e8c5:3538:87a3:aa54:7dfb:8008:fb2e"  # Replace with peer's Yggdrasil IP
    peer_manager.add_peer(peer_ip, 12345)
    #peer_ip = "200:170:d1b:9552:79e7:2726:50aa:4f48"  # Replace with peer's Yggdrasil IP
    #peer_manager.add_peer(peer_ip, 12345)

    # Set the message callback function
    peer_manager.set_message_callback(message_handler)

    # Start the PeerManager's services
    peer_manager.start()

    # Start continuous chat with a peer (Yggdrasil_IP_of_Peer1)
    time.sleep(2)  # Wait for status updates

    while True:
        message = input("You: ")  # Get message from the user
        if message.lower() == 'quit':
            print("Exiting chat...")
            break
        peer_manager.send_message(peer_ip, message)  # Use PeerManager to send the message

