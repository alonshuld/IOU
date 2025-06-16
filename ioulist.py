# !/usr/bin/env python


"""
This file implements an IOU list class
"""


from typing import Dict
from ioulog import IOULog


NAME_KEY = "name"
USERS_KEY = "users"


class IOUList:
    def __init__(self):
        self._iou_list: Dict[str, IOULog] = {}

    
    def get_user(self, name: str) -> Dict:
        """Gives a json formatted information about user

        :param name: Name of the user
        :return: A json formatted dict
        """
        if name not in self._iou_list.keys():
            raise ValueError(f"{name} is not a user")
        
        ans = {}
        ans[NAME_KEY] = name
        ans.update(self._iou_list[name].model_dump())
        return ans


    
    def update_amount(self, name: str):
        """Update the balance field

        :param name: Name of the user we want to update
        """
        self._iou_list[name].balance = sum(self._iou_list[name].owed_by.keys()) - sum(self._iou_list[name].owes.keys())
    

    def create_iou(self, lender: str, borrower: str, amount: float) -> Dict:
        """Create a IOU in the list

        :param lender: The name of the lender
        :param borrower: The name of the borrower
        :param amount: the amount of money to owe
        :return: Updated logs of lender and borrower
        """

        # Validation checks
        if lender not in self._iou_list.keys():
            raise ValueError(f"{lender} is not a valid user")
        
        if borrower not in self._iou_list.keys():
            raise ValueError(f"{borrower} is not a valid user")
        
        if amount <= 0:
            raise ValueError("Amount should be greater than 0")
        
        if borrower in self._iou_list[lender].owed_by.keys():
            self._iou_list[lender].owed_by[borrower] += amount
        else:
            self._iou_list[lender].owed_by[borrower] = amount
        
        self.update_amount(lender)

        if lender in self._iou_list[borrower].owes.keys():
            self._iou_list[borrower].owes[lender] += amount
        else:
            self._iou_list[borrower].owes[lender] = amount
        
        self.update_amount(borrower)

        ans = {}
        ans[USERS_KEY] = []
        for name in sorted([lender, borrower]):
            ans[USERS_KEY].append(self.get_user(name))

        return ans