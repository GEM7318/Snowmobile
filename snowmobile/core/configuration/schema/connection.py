"""
Module contains the object model for **snowmobile.toml**.
"""
from __future__ import annotations

from typing import Dict

from pydantic import Field

from .base import Base


# TODO: type hints/updated docstrings
# noinspection PyUnresolvedReferences
class Credentials(Base):
    """Represents a set of `Snowflake` credentials.

    Attributes:
        user (str):
            Snowflake user.
        password (str):
            Snowflake password.
        role (str):
            Snowflake role.
        account (str):
            Snowflake account.
        warehouse(str):
            Warehouse.
        database (str):
            Database.
        schema_name (str):
            Schema.

    """

    # fmt: off
    _alias: str = Field(
        default_factory=str, alias="_alias"
    )
    user: str = Field(
        default_factory=str, alias='user',
    )

    password: str = Field(
        default_factory=str, alias='password',
    )

    role: str = Field(
        default_factory=str, alias='role',
    )

    account: str = Field(
        default_factory=str, alias='account',
    )

    warehouse: str = Field(
        default_factory=str, alias='warehouse',
    )

    database: str = Field(
        default_factory=str, alias='database',
    )

    schema_name: str = Field(
        default_factory=str, alias='schema',
    )
    # fmt: on

    def as_nm(self, n: str):
        """Sets the credentials alias."""
        self._alias = n
        return self

    @property
    def credentials(self):
        """Returns namespace as a dictionary, excluding :attr:`_alias`."""
        return {k: v for k, v in self.dict(by_alias=True).items() if k != "_alias"}

    def __str__(self):
        """Altering inherited str method to mask credentials detail."""
        attrs = "\n".join(
            f"\t\t{k}='{'*' * len(v) if k != 'alias' else v}'"
            for k, v in vars(self).items()
        )
        return f"Credentials(\n{attrs}\n)"

    def __repr__(self):
        return self.__str__()


class Connection(Base):
    """Represents the full **[credentials]** block within **snowmobile.toml**.

    This includes the :attr:`default_alias` which is the set of credentials
    that :mod:`snowmobile` will authenticate with if :attr:`creds` is not
    explicitly passed.

    Attributes:
        default_alias (str):
            The set of credentials that is used if :attr:`creds` is not
            explicitly passed to :class:`snowmobile.Connect` on
            instantiation.
        creds (str):
            The name given to the set of credentials within the
            **credentials** block of the **snowmobile.toml** file (e.g.
            [credentials.creds] assigns an :attr:`creds` to a given set of
            credentials.
        creds (dict[str, Creds]):
            A dictionary of :attr:`creds` to the associated
            :class:`Creds` object containing its credentials.

    """

    # fmt: off
    default_alias: str = Field(
        default_factory=str, alias='default-creds'
    )

    creds: str = Field(
        default_factory=str, alias='creds'
    )

    credentials: Dict[str, Credentials] = Field(
        default_factory=dict, alias="stored-credentials"
    )

    defaults: Dict = Field(
        default_factory=dict, alias="default-settings"
    )
    # fmt: on

    def __init__(self, **data):

        super().__init__(**data)

        for k, v in data["credentials"].items():
            self.credentials[k] = Credentials(**v).as_nm(n=k)

        if not self.default_alias:
            self.default_alias = list(self.credentials)[0]

    def get(self, creds: str) -> Credentials:
        """Gets and sets a set of credentials given an creds.

        Args:
            creds (str): The name of the set of :attr:`Creds` to
            authenticate with.

        Returns:
            :class:`Creds` object for the creds provided.

        """
        self.creds = creds or self.default_alias
        try:
            return self.credentials[self.creds]
        except KeyError as e:
            raise KeyError(e)
        # return self.__getitem__(self.creds)

    @property
    def current(self):
        """Returns current credentials."""
        return self.get(self.creds)

    # def __getitem__(self, item):
    #     try:
    #         return self.credentials[item]
    #     except KeyError as e:
    #         raise KeyError(e)
