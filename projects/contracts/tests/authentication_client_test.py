from dotenv import load_dotenv
from decouple import config as conf
from algosdk import atomic_transaction_composer, mnemonic, transaction
import pytest
from algokit_utils import Account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient

from smart_contracts.artifacts.authentication.authentication_client import (
    AuthenticationClient,
)

load_dotenv()


@pytest.fixture(scope="session")
def live_account() -> Account:
    mnemonic_phrase = conf("DEPLOYER_MNEMONIC")
    assert mnemonic_phrase, "DEPLOYER_MNEMONIC environment variable not set"
    return Account(private_key=mnemonic.to_private_key(mnemonic_phrase))


@pytest.fixture(scope="session")
def authentication_client(
    algod_client: AlgodClient, live_account: Account
) -> AuthenticationClient:
    config.configure(
        debug=True,
        trace_all=True,
    )

    client = AuthenticationClient(
        algod_client, app_id=728343574, signer=live_account, sender=live_account.address
    )

    # client.deploy(
    #     update_args=Deploy[UpdateArgs](args=UpdateArgs()),
    #     delete_args=Deploy[DeleteArgs](args=DeleteArgs()),
    #     on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    #     on_update=algokit_utils.OnUpdate.AppendApp,
    # )
    return client


def test_update(authentication_client: AuthenticationClient) -> None:
    authentication_client.update_update()


def test_create_algo_id(
    authentication_client: AuthenticationClient, live_account: Account
):
    result = authentication_client.create_algo_id(
        unit_name="AID-01",
        full_name="Ezekiel Victor",
        metadata_url="https://example.com",
    )

    sp = authentication_client.algod_client.suggested_params()

    optin_txn = transaction.AssetOptInTxn(
        sender=live_account.address, sp=sp, index=result.return_value
    )

    optin_txn = optin_txn.sign(live_account.private_key)

    txn_id = authentication_client.algod_client.send_transaction(optin_txn)
    transaction.wait_for_confirmation(
        authentication_client.algod_client, txid=txn_id, wait_rounds=4
    )

    result2 = authentication_client.tranfer_algo_id_token(
        user_address=live_account.address, asset=result.return_value
    )

    print(
        "Created AlgoID asset ID: ",
        result.return_value,
        "Status: ",
        result2.return_value,
    )


#
#
# def test_simulate_says_hello_with_correct_budget_consumed(
#     authentication_client: AuthenticationClient, algod_client: AlgodClient
# ) -> None:
#     result = (
#         authentication_client.compose().hello(name="World").hello(name="Jane").simulate()
#     )
#
#     assert result.abi_results[0].return_value == "Hello, World"
#     assert result.abi_results[1].return_value == "Hello, Jane"
#     assert result.simulate_response["txn-groups"][0]["app-budget-consumed"] < 100
