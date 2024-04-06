import datetime
import uuid
from typing import Literal

from pydantic import BaseModel, Field


class Account(BaseModel):
    name: str
    iban: str = Field(..., serialization_alias="IBAN")
    bic: str = Field(..., serialization_alias="BIC")
    creditor_id: str | None = None


class TransactionConfig(BaseModel):
    batch: bool = True
    currency: str = "EUR"


class AddressLines(BaseModel):
    lines: list[str]


class Address(BaseModel):
    address_type: Literal["ADDR", "PBOX", "HOME", "BIZZ", "MLTO", "DLVY"]
    department: str | None = None
    subdepartment: str | None = None
    street_name: str
    building_number: str
    postcode: str
    town: str
    country: str # country code
    country_subdivision: str | None = None
    lines: AddressLines | None = None


class PaymentBase(BaseModel):
    amount: int
    sequence_type: Literal["FRST", "RCUR", "OOFF", "FNAL"] = Field(..., serialization_alias="type")
    collection_date: datetime.date = datetime.date.today()
    description: str
    endtoend_id: str = uuid.uuid1().hex


class Mandate(BaseModel):
    mandate_id: str
    mandate_date: datetime.date = datetime.date.today()


class DirectDebit(Mandate, PaymentBase, TransactionConfig, Account):
    pass
