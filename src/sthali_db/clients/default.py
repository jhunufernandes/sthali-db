"""This module provides the client class for interacting with a virtual database."""
import typing

from . import Base, PaginateParameters, Partial, ResourceId, ResourceObj


class DefaultClient(Base):
    """A class representing a virtual DB client for database operations.

    Attributes:
        db (dict): A dictionary representing the database.

    Args:
        _ (str): A placeholder argument.
        table (str): The name of the table.

    Raises:
        self.exception: If the resource is not found in the database.
    """

    _db: typing.ClassVar[dict[ResourceId, ResourceObj]] = {}

    def __init__(self, _: str, table: str) -> None:
        """Initialize a DefaultClient instance.

        Args:
            _ (str): A placeholder argument.
            table (str): The name of the table.

        Returns:
            None
        """
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
            return self._db[resource_id]
        except KeyError as exception:
            raise self.exception(self.status.HTTP_404_NOT_FOUND, "not found") from exception

    async def insert_one(self, resource_id: ResourceId, resource_obj: ResourceObj) -> ResourceObj:
        """Inserts a resource object in the database.

        Args:
            resource_id (ResourceId): The ID of the resource to be inserted.
            resource_obj (ResourceObj): The resource object to be inserted.

        Raises:
            self.exception: If the resource already exists in the database.

        Returns:
            ResourceObj: The resource object containing the ID.
        """
        try:
            self._get(resource_id)
        except self.exception:
            self._db[resource_id] = resource_obj
            return {"id": resource_id, **resource_obj}
        else:
            raise self.exception(self.status.HTTP_409_CONFLICT, "conflict")

    async def select_one(self, resource_id: ResourceId) -> ResourceObj:
        """Retrieves a resource from the database based on the given ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be retrieved.

        Returns:
            ResourceObj: The retrieved resource object.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        resource_obj = self._get(resource_id)
        return {"id": resource_id, **resource_obj}

    async def update_one(
        self,
        resource_id: ResourceId,
        resource_obj: ResourceObj,
        partial: Partial = None,
    ) -> ResourceObj:
        """Updates a resource in the database based on the given ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be updated.
            resource_obj (ResourceObj): The resource object to be updated.
            partial (Partial): Whether to perform a partial update or replace the entire resource object.
                Defaults to None.

        Raises:
            self.exception: If the resource is not found in the database.

        Returns:
            ResourceObj: The resource object containing the ID.
        """
        _resource_obj = self._get(resource_id)
        if partial:
            _resource_obj.update(resource_obj)
        else:
            _resource_obj = resource_obj
        self._db[resource_id] = _resource_obj
        return {"id": resource_id, **_resource_obj}

    async def delete_one(self, resource_id: ResourceId) -> None:
        """Deletes a resource from the database based on the given resource ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be deleted.

        Raises:
            self.exception: If the resource is not found in the database.

        Returns:
            None
        """
        self._get(resource_id)
        self._db.pop(resource_id, None)

    async def select_many(self, paginate_parameters: PaginateParameters) -> list[ResourceObj]:
        """Retrieves multiple resources from the database based on the given pagination parameters.

        Args:
            paginate_parameters (PaginateParameters): The pagination parameters.

        Returns:
            list[ResourceObj]: A list of objects representing the retrieved resources.
        """
        return [{"id": k, **v} for k, v in self._db.items()][paginate_parameters.skip : paginate_parameters.limit]
