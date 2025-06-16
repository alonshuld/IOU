# !/usr/bin/env python


from pydantic import BaseModel
from typing import Dict


"""
This file implements an IOU log class
"""


class IOULog(BaseModel):
    """
    IOU Log class
    """
    owes: Dict[str, float] = {}
    owed_by: Dict[str, float] = {}
    balance: float = 0
