from typing import Dict, Optional, List
from ..schemas.user import UserCreate, UserInDB, UserUpdate
from ..security import get_password_hash

fake_users_db: Dict[int, UserInDB] = {}
next_user_id = 1

def init_db():
    global next_user_id
    if not get_user_by_email("admin@example.com"):
        admin_user = UserCreate(
            email="admin@example.com",
            full_name="Admin User",
            password="a-very-secure-password",
            role="admin"
        )
        create_user(admin_user)
        print(f"🔑 Usuário admin criado: admin@example.com / a-very-secure-password")

def get_user_by_email(email: str) -> Optional[UserInDB]:
    for user in fake_users_db.values():
        if user.email == email:
            return user
    return None

def get_user(user_id: int) -> Optional[UserInDB]:
    return fake_users_db.get(user_id)

def get_all_users() -> List[UserInDB]:
    return list(fake_users_db.values())

def create_user(user_in: UserCreate) -> UserInDB:
    global next_user_id
    hashed_password = get_password_hash(user_in.password)
    user_db = UserInDB(
        id=next_user_id,
        hashed_password=hashed_password,
        **user_in.model_dump(exclude={"password"})
    )
    fake_users_db[next_user_id] = user_db
    next_user_id += 1
    return user_db

def update_user(user_id: int, user_in: UserUpdate) -> Optional[UserInDB]:
    db_user = get_user(user_id)
    if not db_user:
        return None
    
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    fake_users_db[user_id] = db_user
    return db_user

def update_user_password(user_id: int, new_password: str) -> UserInDB:
    db_user = get_user(user_id)
    db_user.hashed_password = get_password_hash(new_password)
    fake_users_db[user_id] = db_user
    return db_user

def delete_user(user_id: int) -> Optional[UserInDB]:
    if user_id in fake_users_db:
        return fake_users_db.pop(user_id)
    return None