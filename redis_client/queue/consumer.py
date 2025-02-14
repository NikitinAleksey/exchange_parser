__all__ = ["RedisConsumer"]


class RedisConsumer:
    def __init__(self, redis_client, queue_name: str):
        self.client = redis_client
        self.queue_name = queue_name

    async def pop(self, timeout: int = 0):
        """Получить сообщение из очереди (блокирующий вызов)"""
        result = await self.client.brpop(self.queue_name, timeout=timeout)
        return result[1] if result else None

    async def process_queue(self, handler):
        """Фоновый обработчик очереди"""
        while True:
            message = await self.pop(timeout=5)
            if message:
                await handler(message)
