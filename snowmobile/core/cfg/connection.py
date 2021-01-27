"""
[connection] section from **snowmobile.toml**, including subsections.
"""
from __future__ import annotations

from typing import Dict

from pydantic import Field

from .base import Base


class Credentials(Base):
    """[connection.credentials.credentials_alias]"""

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
        return f"Credentials('{self._alias}')"

    def __repr__(self):
        return f"Credentials('{self._alias}')"


class Connection(Base):
    """[connection]

    This includes the :attr:`default_alias` which is the set of credentials
    that :mod:`snowmobile` will authenticate with if :attr:`creds` is not
    explicitly passed.

    Attributes:
        default_alias (str):
            The set of credentials that is used if :attr:`creds` is not
            explicitly passed to :class:`snowmobile.connect` on
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
    provided_alias: str = Field(
        default_factory=str, alias='provided-creds'
    )
    credentials: Dict[str, Credentials] = Field(
        default_factory=dict, alias="stored-credentials"
    )
    defaults: Dict = Field(
        default_factory=dict, alias="default-arguments"
    )
    # fmt: on

    def __init__(self, **data):

        super().__init__(**data)

        for k, v in data["credentials"].items():
            self.credentials[k] = Credentials(**v).as_nm(n=k)

        if not self.default_alias:
            self.default_alias = list(self.credentials)[0]

    @property
    def creds(self):
        """Credentials alias used by current Connection."""
        return self.provided_alias or self.default_alias

    @property
    def current(self):
        """Returns current credentials."""
        try:
            return self.credentials[self.creds]
        except KeyError as e:
            raise e
        # return self.get(self.creds)

    @property
    def connect_kwargs(self) -> Dict:
        """Arguments from snowmobile.toml for `snowflake.connector.connect()`."""
        return {**self.defaults, **self.current.credentials}
