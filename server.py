# !/usr/bin/env python


"""
This file lets the IOU work with FastApi
"""


from typing import List, Dict, Optional
from fastapi import FastAPI, Query, HTTPException
from ioulist import IOUList


USERS_KEY = "users"
NOT_FOUND_ERROR = 404


# Global Variables
iou_db = IOUList()
app = FastAPI()


@app.get("/users")
async def get_users(users: Optional[List[str]] = Query(default=[])) -> Dict:
    """
    Get the users in the IOU list

    :param users: The users we want to get, if empty returns all the available users, defaults to []
    :return: Dictionary of the requested users
    """
    try:
        result = await iou_db.get_users(users)
    except ValueError as error:
        raise HTTPException(status_code=NOT_FOUND_ERROR, detail=str(error))
    return {USERS_KEY: result}


@app.post("/add")
async def create_user(user: str) -> Dict:
    """
    Create a user in the IOU List

    :param user: Name of the new user
    :return: The object of the created user
    """
    try:
        result = await iou_db.create_user(user)
    except ValueError as error:
        raise HTTPException(status_code=NOT_FOUND_ERROR, detail=str(error))
    return result


@app.post("/iou")
async def create_iou(lender: str, borrower: str, amount: float) -> Dict:
    """
    Create an IOU

    :param lender: Name of the lender
    :param borrower: Name of the borrower
    :param amount: amount of money that borrowed
    :return: The updated users object
    """
    try:
        result = await iou_db.create_iou(lender, borrower, amount)
    except ValueError as error:
        raise HTTPException(status_code=NOT_FOUND_ERROR, detail=str(error))
    return {USERS_KEY: result}
