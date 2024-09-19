# tests/test_peer_manager.py
import unittest
from yggpeer.peer_manager import PeerManager

class TestPeerManager(unittest.TestCase):
    def test_add_peer(self):
        pm = PeerManager(local_port=12345, discovery_port=12344)
        pm.add_peer("::1", 12345)
        self.assertEqual(pm.get_peer_status("::1"), "unknown")

if __name__ == "__main__":
    unittest.main()
