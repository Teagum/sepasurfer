import datetime

import pandas as pd
from sepaxml import SepaDD

from sepasurfer.models import Account, DirectDebit, TransactionConfig
from sepasurfer import utils


class DirectDebitTransaction:
    def __init__(
            self,
            config: TransactionConfig,
            creditor: Account,
            collection_date: datetime.date | None = None,
            schema: str = "pain.008.001.02",
            clean: bool = True
            ) -> None:
        self.config = config
        self.creditor = creditor
        self.schema = schema
        self.clean = clean

        if collection_date is None:
            self.collection_date = datetime.date.today() + datetime.timedelta(days=2)
        else:
            self.collection_date = collection_date

        _config = config.model_dump()
        _config.update(creditor.model_dump(by_alias=True))
        self._sepa = SepaDD(_config, schema=self.schema, clean=self.clean)


    def add(self, item):
        self._sepa.add_payment(item.model_dump(by_alias=True))

    def export(self, validate=True, pretty_print=True):
        return self._sepa.export(validate, pretty_print)

    def debtors_from_df(self, df: pd.DataFrame, description: str
                        ) -> list[DirectDebit]:
        out = []
        for _, member in df.iterrows():
            dd = DirectDebit(
                name=f"{member.Vorname} {member.Nachname}",
                iban=member.IBAN,
                bic=member.BIC,
                amount=utils.contrib(member.Mitgliedsbeitrag),
                collection_date=self.collection_date,
                sequence_type="RCUR",
                mandate_id=str(member.Mandatsreferenz),
                mandate_date=member['Erteilt am'].date(),
                description=description)
            out.append(dd)
        return out
