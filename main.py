import asyncio

from app.application import Application


async def main():
    application = Application()
    return await application.launch()

if __name__ == '__main__':
    asyncio.run(main())
