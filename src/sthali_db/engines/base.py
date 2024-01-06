from typing import NoReturn
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import NonNegativeInt


class BaseEngine:
    exception = HTTPException
    status = status

    def __init__(self, path: str, table: str) -> None:
        pass

    async def insert_one(self, resource_id: UUID, resource_obj: dict) -> NoReturn:
        raise NotImplementedError

    async def select_one(self, resource_id: UUID) -> NoReturn:
        raise NotImplementedError

    async def update_one(self, resource_id: UUID, resource_obj: dict) -> NoReturn:
        raise NotImplementedError

    async def delete_one(self, resource_id: UUID) -> NoReturn:
        raise NotImplementedError

    async def select_many(self, skip: NonNegativeInt = 0, limit: NonNegativeInt = 100) -> NoReturn:
        raise NotImplementedError
