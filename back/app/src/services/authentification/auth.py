from datetime import datetime, timedelta
from typing import Annotated
import bcrypt
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.src.services.tables.user import UserService
from app.src.entities.schemas.user import DecodedUser
from app.src.utils.const import INCORRECT_CREDENTIALS, USER_NOT_FOUND
from app.src.entities.database import get_db

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(self, session: Session = None, form_data: OAuth2PasswordRequestForm = None) -> None:
        self.session = session
        self.form_data = form_data

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta):
        """
        Create a JWT access token with the provided data.

        :param data (dict): Data to be included in the token payload.
        :param expires_delta (timedelta): Expiration time for the token.

        :Returns str: Encoded JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str):
        """
        Decode a JWT token and extract the username,id and role from it.

        :param token (str): JWT token to decode.

        :Returns Client: pydantic schema containing user info

        :Raises HTTPException: If the token is invalid, expired, or the username cannot be extracted.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user = DecodedUser(
                id=payload.get("id"),
                username=payload.get("username"),
            )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not extract username from token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # check if we the user exists in the DB
            with next(get_db()) as session:
                user_exists = UserService(session).get(user.id)

            if user_exists is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=USER_NOT_FOUND,
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> DecodedUser:
        """
            A helper function to return the logged-in user
        """
        user = self.decode_token(token)
        if user is None:
            raise INCORRECT_CREDENTIALS
        return user

    def login_user(self):
        """
        Authenticate a user and generate an access token.

        :Returns dict: Dictionary containing the access token and token type.

        :Raises HTTPException: If the provided username or password is incorrect.
        """
        with next(get_db()) as session:
            user_data = UserService(session).get_user_by_username(self.form_data.username)
        print(user_data)

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INCORRECT_CREDENTIALS,
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not bcrypt.checkpw(self.form_data.password.encode('utf-8'), user_data.hash_password.encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INCORRECT_CREDENTIALS,
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = self.create_access_token(
            {"id": user_data.id, "username": user_data.username, "role": user_data.role}, access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}


AUTH = AuthService()
dp_user = Annotated[DecodedUser, Depends(AUTH.get_current_user)]
