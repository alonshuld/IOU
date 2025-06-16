# !/usr/bin/env python


"""
This file lets the IOU work with FastApi
"""


from typing import List, Dict
from fastapi import FastAPI
from ioulist import IOUList


# Global Variables
iou_db = IOUList()
app = FastAPI()


@app.get("/users")
def get_users(users: List[str] = []) -> Dict:
    """Get the users in the IOU list

    :param users: The users we want to get, if empty returns all the available users, defaults to []
    :return: Dictionary of the requested users
    """
    return iou_db.get_users(users)


@app.post("/add")
def create_user(user: str) -> Dict:
    """Create a user in the IOU List

    :param user: Name of the new user
    :return: The object of the created user
    """
    return iou_db.create_user(user)


@app.post("/iou")
def create_iou(lender: str, borrower: str, amount: float) -> float:
    """Create an IOU

    :param lender: Name of the lender
    :param borrower: Name of the borrower
    :param amount: amount of money that borrowed
    :return: The updated users object
    """
    return iou_db.create_iou(lender, borrower, amount)