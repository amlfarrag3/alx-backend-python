import aiosqlite
import asyncio

async def asyncfetchusers():
    db_path = "example.db"
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def asyncfetcholder_users():
    db_path = "example.db"
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        asyncfetchusers(),
        asyncfetcholder_users()
    )
    print("All users:", users)
    print("Users older than 40:", older_users)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
