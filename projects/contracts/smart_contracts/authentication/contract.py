from algopy import ARC4Contract, Txn, arc4, urange

class Authentication(ARC4Contract):
    def __init__(self) -> None:
        self.admins: arc4.DynamicArray[arc4.Address] = arc4.DynamicArray[arc4.Address]()
        self.admins.append(arc4.Address.from_bytes(Txn.sender.bytes))


    @arc4.abimethod(allow_actions=["UpdateApplication"])
    def update(self) -> bool:
        for index in urange(self.admins.length):
            value = self.admins[index]
            return value.native == Txn.sender
        return False


    @arc4.abimethod(allow_actions=["DeleteApplication"])
    def delete(self) -> bool:
        for index in urange(self.admins.length):
            value = self.admins[index]
            return value.native == Txn.sender
        return False
