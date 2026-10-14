from dataclasses import dataclass


@dataclass
class UserModel:
    user_id: int
    user_name: str
    email: str


@dataclass
class UserWithPasswordModel:
    user_id: int
    user_name: str
    email: str
    password_hash: str


@dataclass
class UserFullModel:
    user_id: int
    user_name: str
    email: str
    password_hash: str
    created_time: int