import pandas as pd
import pytest

from sepasurfer.sepaxml import DirectDebitTransaction
from sepasurfer.models import Account, TransactionConfig

@pytest.fixture
def creditor_account():
    config = TransactionConfig()
    creditor = Account(
        name="Förderverein der Schule Rothestraße e.V.",
        iban="DE65201900030060346701",
        bic="GENODEF1HH2",
        creditor_id="DE26ZZZ00000000000")
    return config, creditor

@pytest.fixture
def ddt(creditor_account):
    return DirectDebitTransaction(*creditor_account)

@pytest.fixture
def member_data():
    return pd.read_pickle("/Users/pmind/fvdsr/data/contrib/2024-02-25/2024-02-25.pkl")


def test_create_dd(creditor_account):
    sepa = DirectDebitTransaction(*creditor_account)


def test_add_payments(ddt, member_data):
    payments = ddt.debtors_from_df(member_data, "Test Beitrag")
    for item in payments:
        ddt.add(item)


def test_export(ddt, member_data):
    payments = ddt.debtors_from_df(member_data, "Test Beitrag")
    for item in payments:
        ddt.add(item)
    ddt.export(validate=True, pretty_print=True)
