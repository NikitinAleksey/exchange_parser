__all__ = ["RedisProducer"]


class RedisProducer:
    def __init__(self, redis_client):
        self.client = redis_client

    async def push(self, message: str, queue_name: str):
        """Добавить сообщение в очередь"""
        await self.client.lpush(queue_name, message)
