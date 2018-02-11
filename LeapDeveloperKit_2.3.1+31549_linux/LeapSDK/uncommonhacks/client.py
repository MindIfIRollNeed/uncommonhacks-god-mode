import enet
host = enet.Host(None, 1, 0, 0)
peer = host.connect(enet.Address("localhost", 33333), 1)