from unittest import IsolatedAsyncioTestCase, mock
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from sthali_db import clients


class TestBase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        base = clients.Base(path="path", table="table")
        self.base = base

    async def test_return_default(self) -> None:
        self.assertEqual(self.base.exception, clients.HTTPException)
        self.assertEqual(self.base.status, clients.status)

    async def test_insert_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.insert_one(resource_id=uuid4(), resource_obj={})

    async def test_select_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.insert_one(resource_id=uuid4(), resource_obj={})

    async def test_update_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.insert_one(resource_id=uuid4(), resource_obj={})

    async def test_delete_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.insert_one(resource_id=uuid4(), resource_obj={})

    async def test_select_many_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.insert_one(resource_id=uuid4(), resource_obj={})


class TestDBSpecification(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        db_spec = clients.DBSpecification(path="path")  # type: ignore

        self.assertEqual(db_spec.path, "path")
        self.assertEqual(db_spec.client, "Default")

    async def test_return_custom(self) -> None:
        db_spec = clients.DBSpecification(path="path", client="TinyDB")

        self.assertEqual(db_spec.path, "path")
        self.assertEqual(db_spec.client, "TinyDB")


class TestDB(IsolatedAsyncioTestCase):
    class MockDefaultClient:
        insert_one = AsyncMock(return_value="insert_one")
        select_one = AsyncMock(return_value="select_one")
        update_one = AsyncMock(return_value="update_one")
        delete_one = AsyncMock(return_value="delete_one")
        select_many = AsyncMock(return_value="select_many")

    @mock.patch("sthali_db.clients.default.DefaultClient")
    def setUp(self, mocked_client: MagicMock) -> None:
        mocked_client.return_value = self.MockDefaultClient()
        db_spec = clients.DBSpecification(path="path")  # type: ignore
        self.db = clients.DB(db_spec=db_spec, table="table")  # type: ignore

    async def test_return_default(self) -> None:
        self.assertTrue(isinstance(self.db.client, self.MockDefaultClient))

    async def test_select_one(self) -> None:
        result = await self.db.select_one()

        self.assertEqual(result, "select_one")

    async def test_update_one(self) -> None:
        result = await self.db.update_one()

        self.assertEqual(result, "update_one")

    async def test_delete_one(self) -> None:
        result = await self.db.delete_one()

        self.assertEqual(result, "delete_one")

    async def test_select_many(self) -> None:
        result = await self.db.select_many()

        self.assertEqual(result, "select_many")
