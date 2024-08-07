"""This module provides the client class for interacting with a TinyDB database."""
from tinydb import Query, TinyDB

from . import Base, PaginateParameters, Partial, ResourceId, ResourceObj


class TinyDBclient(Base):
    """A class representing a TinyDB client for database operations.

    Args:
        path (str): The path to the TinyDB database file.
        table (str): The name of the table in the database.

    Attributes:
        db (TinyDB): The TinyDB instance.
        path (str): The path to the TinyDB database file.
        table (str): The name of the table in the database.
    """

    db: TinyDB
    path: str
    table: str

    def __init__(self, path: str, table: str) -> None:
        """Initialize the TinyDBclient class.

        Args:
            path (str): The path to the database.
            table (str): The name of the table in the database.

        """
        self.db = TinyDB(path)
        self.table = table

    def _get(self, resource_id: ResourceId) -> ResourceObj:
        """Retrieves a resource from the database based on the given resource ID.

        Args:
            resource_id (ResourceId): The ID of the resource to retrieve.

        Returns:
            ResourceObj: The retrieved resource.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        try:
            result = self.db.table(self.table).search(Query().resource_id == str(resource_id))  # type: ignore
            return result[0]
        except (KeyError, IndexError) as exception:
            raise self.exception(self.status.HTTP_404_NOT_FOUND, "not found") from exception

    async def insert_one(self, resource_id: ResourceId, resource_obj: ResourceObj) -> ResourceObj:
        """Inserts a resource object in the database.

        Args:
            resource_id (ResourceId): The ID of the resource to be inserted.
            resource_obj (ResourceObj): The resource object to be inserted.

        Returns:
            ResourceObj: The resource object containing the ID.

        Raises:
            self.exception: If the resource already exists in the database.
        """
        self.db.table(self.table).insert({"resource_id": str(resource_id), "resource_obj": resource_obj})  # type: ignore
        return {"id": resource_id, **resource_obj}

    async def select_one(self, resource_id: ResourceId) -> ResourceObj:
        """Retrieves a resource from the database based on the given ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be retrieved.

        Returns:
            ResourceObj: The retrieved resource object.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        result = self._get(resource_id)
        return {"id": resource_id, **result["resource_obj"]}

    async def update_one(
        self, resource_id: ResourceId, resource_obj: ResourceObj, partial: Partial = None
    ) -> ResourceObj:
        """Updates a resource in the database based on the given ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be updated.
            resource_obj (ResourceObj): The resource object to be updated.
            partial (Partial): Whether to perform a partial update or replace the entire resource object.
                Defaults to None.

        Returns:
            ResourceObj: The resource object containing the ID.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        _resource_obj = self._get(resource_id)
        if partial:
            _resource_obj.update(resource_obj)
        else:
            _resource_obj = resource_obj
        self.db.table(self.table).update({"resource_obj": _resource_obj}, Query().resource_id == str(resource_id))  # type: ignore
        return {"id": resource_id, **_resource_obj}

    async def delete_one(self, resource_id: ResourceId) -> None:
        """Deletes a resource from the database based on the given resource ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be deleted.

        Returns:
            None

        Raises:
            self.exception: If the resource is not found in the database.
        """
        self._get(resource_id)
        self.db.table(self.table).remove(Query().resource_id == str(resource_id))  # type: ignore

    async def select_many(self, paginate_parameters: PaginateParameters) -> list[ResourceObj]:
        """Retrieves multiple resources from the database based on the given pagination parameters.

        Args:
            paginate_parameters (PaginateParameters): The pagination parameters.

        Returns:
            list[ResourceObj]: A list of objects representing the retrieved resources.
        """
        return [{"id": result["resource_id"], **result["resource_obj"]} for result in self.db.table(self.table).all()][
            paginate_parameters.skip : paginate_parameters.limit
        ]  # type: ignore
