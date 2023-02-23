from typing import TypeAlias
from typing import Union

from canonical import EmailAddress
from headless.ext.oauth2.models import SubjectIdentifier

from .publicidentifier import PublicIdentifier


PrincipalType: TypeAlias = Union[
    EmailAddress,
    SubjectIdentifier,
    PublicIdentifier
]