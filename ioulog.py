# !/usr/bin/env python


"""
This file implements an IOU log class
"""


from pydantic import BaseModel
from typing import Dict


class IOULog(BaseModel):
    """
    IOU Log that holds all the transactions
    """
    owes: Dict[str, float] = {}
    owed_by: Dict[str, float] = {}
    balance: float = 0


    def _update_amount(self):
        """
        Update the balance field

        :param name: Name of the user we want to update
        """
        self.balance = sum(self.owed_by.values()) - sum(self.owes.values())
