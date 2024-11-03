from algopy import ARC4Contract, Global, Txn, arc4, itxn, urange
from algopy.op import ITxn


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

    @arc4.abimethod()
    def create_algo_id(
        self,
        user_address: arc4.Address,
        unit_name: arc4.String,
        full_name: arc4.String,
        metadata_url: arc4.String,
    ) -> arc4.UInt64:
        algo_id_txn = itxn.AssetConfig(
            total=1,
            fee=1000,
            url=metadata_url.native,
            unit_name=unit_name.native,
            asset_name=full_name.native,
            manager=Global.current_application_address,
            reserve=Global.current_application_address,
            freeze=Global.current_application_address,
            clawback=Global.current_application_address,
        )
        algo_id_txn.submit()
        asset = ITxn.created_asset_id()

        asset_freeze_txn = itxn.AssetFreeze(
            freeze_account=user_address.native,
            freeze_asset=asset,
            frozen=True,
            fee=1000,
        )
        asset_freeze_txn.submit()
        return arc4.UInt64(asset.id)

    # def accpt_payment(self, txn: gtxn.PaymentTransaction):
    #     assert txn.sender === "soem"
    #     assert txn.amount === 1020202301
