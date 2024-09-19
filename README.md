# YggPeer

YggPeer is a Python library for peer-to-peer communication over the Yggdrasil network, providing easy-to-use tools for status management, messaging, and chat between peers.

## Features
- Integration with [Yggdrasil](https://yggdrasil-network.github.io/)
- Peer-to-peer messaging
- Status management (available, busy, etc.)

## Installation

Install YggPeer using pip:

```bash
pip install yggpeer
```

## Example

```python
# example_chat.py
from yggpeer import PeerManager
import time

def example_chat():
    peer_manager = PeerManager(local_port=12345, discovery_port=10799)

    # Add a peer (Yggdrasil IP and chat port)
    peer_manager.add_peer("Yggdrasil_IP_of_Peer", 12345)

    # Start the PeerManager services
    peer_manager.start()

    # Start sending messages to the peer
    time.sleep(2)  # Wait for the services to initialize

    while True:
        message = input("You: ")
        if message.lower() == 'quit':
            print("Exiting chat...")
            break
        peer_manager.send_message("Yggdrasil_IP_of_Peer", message)

if __name__ == "__main__":
    example_chat()

```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


