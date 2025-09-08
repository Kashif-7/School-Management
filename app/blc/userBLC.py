from app.repository.user_repository import UserRepository


class UserBLC:
    @staticmethod
    def user_signup(args: dict):
        user = UserRepository.user_signup(args)
        return {"user_id": user, "message": "User created successfully"}
    
    @staticmethod
    def user_login(args: dict):
        user = UserRepository.user_login(args)
        return user  
