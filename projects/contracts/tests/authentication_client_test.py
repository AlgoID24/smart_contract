import os
import algokit_utils
import pytest
from algosdk import mnemonic
from algokit_utils import Account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.authentication.authentication_client import AuthenticationClient, DeleteArgs, Deploy, UpdateArgs

@pytest.fixture(scope="session")
def live_account() -> Account:
    mnemonic_phrase = os.getenv("KODES_ENVIRONMENT")
    assert mnemonic_phrase, "KODES_ENVIRONMENT: Error"
    return Account(private_key = mnemonic.to_private_key(mnemonic_phrase))


@pytest.fixture(scope="session")
def authentication_client(
    algod_client: AlgodClient, live_account: Account,
) -> AuthenticationClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = AuthenticationClient(
        algod_client,
        app_id = 728344999,
        signer= live_account,
        sender= live_account.address,
    )

    # client.deploy(
    #     update_args=Deploy[UpdateArgs](args=UpdateArgs()),
    #     delete_args=Deploy[DeleteArgs](args=DeleteArgs()),
    #     on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    #     on_update=algokit_utils.OnUpdate.AppendApp,
    # )
    return client


def test_update(authentication_client: AuthenticationClient) -> None:
    result = authentication_client.update_update()

    assert result.return_value == "Hello, World"
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
