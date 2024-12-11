from ..components import Controller, Network

def create_network():
    rede = Network()
    controlador = Controller(rede)
    row, col = 3, 4
    rede.set_ready_topology("Grade", row, col)
    rede.draw()
