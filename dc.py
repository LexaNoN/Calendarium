from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from texts import Text


class Permissons(Enum):
    BANNED = 0
    REGISTRATION = 1
    USER = 2
    MODERATOR = 3
    ADMIN = 4


@dataclass
class User:
    id: int = 0
    permission: Permissons = Permissons.USER
    id_telegram: int = 0
    nickname: str = ''
    stage: str = ''
    date_reg: datetime = None
