import bcrypt
import jwt


def encode_jwt(
    payload: dict,
    private_key: str,
    algorithm: str,
):
    encoded = jwt.encode(payload=payload,
                         key=private_key,
                         algorithm=algorithm
    )
    return encoded

def decoded_jwt(
    token: str | bytes,
    public_key: str,
    algorithm: str,
):
    decoded = jwt.decode(jwt=token,
                         key=public_key,
                         algorithms=[algorithm])
    return decoded


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(password=pwd_bytes,
                         salt=salt)

def valodate_password(
    password: str,
    hashed_password: bytes,) -> bool:
    return bcrypt.checkpw(password=password.encode,
                          hashed_password=hash_password,)