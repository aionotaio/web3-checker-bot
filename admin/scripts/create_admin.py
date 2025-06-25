import asyncio
import getpass

from shared.session import get_admin_db
from shared.schemas import AdminUser, AdminAuth
from shared.exceptions import AlreadyExistsError
from admin.services.auth import get_password_hash


collection = get_admin_db()


async def create_admin(auth_data: AdminAuth) -> None:
    existing = await collection.find_one({"username": auth_data.username})
    if existing:
        raise AlreadyExistsError("Admin already exists!")

    hashed_password = get_password_hash(auth_data.password)

    admin = AdminUser(username=auth_data.username, hashed_password=hashed_password)

    result = await collection.insert_one(admin.model_dump())

    print('Successfully created!') if result.inserted_id else print('Failed to create, try again.')


if __name__ == "__main__":
    username = input("Enter admin username (don't forget to save it!): ")
    password = getpass.getpass("Enter password from 5 to 32 characters (don't forget to save it!): ")
    asyncio.run(create_admin(AdminAuth(username=username, password=password)))
