import asyncio
import aiosqlite

async def async_fetch_users(db):
    async with db.execute("SELECT * FROM users") as cursor:
        rows = await cursor.fetchall()
        return rows

async def async_fetch_older_users(db):
    async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
        rows = await cursor.fetchall()
        return rows

async def fetch_concurrently():
    async with aiosqlite.connect("example.db") as db:
        tasks = [
            async_fetch_users(db),
            async_fetch_older_users(db)
        ]
        results = await asyncio.gather(*tasks)
        return results

async def main():
    results = await fetch_concurrently()
    users, older_users = results
    print("All Users:")
    for user in users:
        print(user)
    print("\nOlder Users:")
    for user in older_users:
        print(user)

asyncio.run(main())
