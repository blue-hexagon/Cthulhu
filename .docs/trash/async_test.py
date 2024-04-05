import asyncio


async def main():
    task = asyncio.create_task(main2())
    print("A")
    print("B")
    await task


async def main2():
    print("1")
    await asyncio.sleep(1)
    print("2")


if __name__ == "__main__":
    asyncio.run(main())
