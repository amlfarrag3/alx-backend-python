import aiosqlite
import asyncio

async def fetch_concurrently():
    db_path = "example.db"

    async def fetch_all_users():
        async with aiosqlite.connect(db_path) as db:
            async with db.execute("SELECT * FROM users") as cursor:
                return await cursor.fetchall()

    async def fetch_users_older_than_40():
        async with aiosqlite.connect(db_path) as db:
            async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
                return await cursor.fetchall()

    results = await asyncio.gather(
        fetch_all_users(),
        fetch_users_older_than_40()
    )

    print("All users:", results[0])
    print("Users older than 40:", results[1])

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

    
  
