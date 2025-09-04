from pymongo.client_session import ClientSession
from app.repository.user_repository import UserRepository


class UserBLC:
    @staticmethod
    def user_signup(args: dict, session: ClientSession):
        user = UserRepository.user_signup(args, session=session)
        return {"user_id": user, "message": "User created successfully"}
    
    @staticmethod
    def user_login(args: dict, session: ClientSession):
        user = UserRepository.user_login(args, session=session)
        return user  
