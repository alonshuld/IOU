# !/usr/bin/env python


"""
This file implements an IOU list class
"""


from typing import Dict, List
from ioulog import IOULog


NAME_KEY = "name"


class IOUList:
    def __init__(self):
        self._iou_list: Dict[str, IOULog] = {}

    
    def _get_user(self, name: str) -> Dict:
        """Gives a json formatted information about user

        :param name: Name of the user
        :return: A json formatted dict
        """
        if name not in self._iou_list.keys():
            raise ValueError(f"{name} is not a user")

        return {NAME_KEY: name, **self._iou_list[name].model_dump()}

    
    def _update_amount(self, name: str):
        """Update the balance field

        :param name: Name of the user we want to update
        """
        self._iou_list[name].balance = sum(self._iou_list[name].owed_by.values()) - sum(self._iou_list[name].owes.values())
    

    def _is_valid_name(self, name: str):
        """checks if the name is in the list

        :param name: the name we want to check
        :raises ValueError: if not found raises a error
        """
        if name not in self._iou_list:
            raise ValueError(f"{name} is not a valid user")
    

    def _is_valid_amount(self, amount: float):
        """Checks if the amount is valid

        :param amount: the amount we want to check
        :raises ValueError: if the value is not greater than 0
        """
        if amount <= 0:
            raise ValueError("Amount should be greater than 0")
    

    def _update_borrower(self, lender: str, borrower: str, amount: float):
        """Updates the borrower statistic

        :param lender: The user that lends the money
        :param borrower: The user that borrows the money
        :param amount: The amount of borrow
        """
        if lender in self._iou_list[borrower].owes.keys():
            self._iou_list[borrower].owes[lender] += amount
        else:
            self._iou_list[borrower].owes[lender] = amount
        self._update_amount(borrower)

    
    def _update_lender(self, lender: str, borrower: str, amount: float):
        """Updates the lender statistic

        :param lender: The user that lends the money
        :param borrower: The user that borrows the money
        :param amount: The amount of borrow
        """
        if borrower in self._iou_list[lender].owed_by.keys():
            self._iou_list[lender].owed_by[borrower] += amount
        else:
            self._iou_list[lender].owed_by[borrower] = amount
        self._update_amount(lender)

    
    async def create_iou(self, lender: str, borrower: str, amount: float) -> Dict:
        """Create a IOU in the list

        :param lender: The name of the lender
        :param borrower: The name of the borrower
        :param amount: the amount of money to owe
        :return: Updated logs of lender and borrower
        """

        # Validation checks
        for name in [lender, borrower]:
            self._is_valid_name(name)
        self._is_valid_amount(amount)
        
        self._update_borrower(lender, borrower, amount)
        self._update_lender(lender, borrower, amount)

        return [self._get_user(lender), self._get_user(borrower)]
    

    async def get_users(self, names: List[str] = []) -> Dict:
        """Get list of users

        :param names: Names of the users we want to get, if empty gets all the users
        :return: Dictionary of all the requested users
        """
        # If names is empty give all the available users
        if len(names) == 0:
            names = self._iou_list.keys()

        answer = []
        for name in sorted(names):
            answer.append(self._get_user(name))

        return answer


    async def create_user(self, name: str) -> Dict:
        """Create a new user

        :param name: new unique username
        :return: The created user object
        """
        # Validation check
        if name in self._iou_list.keys():
            raise ValueError(f"{name} is already taken")
        
        self._iou_list[name] = IOULog()

        return self._get_user(name)