from redis_client import RedisCache

__all__ = ["QueueController"]


class QueueController:
    def __init__(
            self,
    ):
        ...

    async def publish_event(self, queue_name: str):
        """Публикует какое-то событие в очереди. По задумке нужен, чтобы публиковать сообщение о том,
        что пришло согласие пользователя на покупку/продажу. Возможно, тут лучше будет не очередь, а прямая команда,
        что надо сделать. А очереди оставим только для бирж."""
        ...

    async def subscribe_queue(self, queue_name: str):
        """Подписывается на очередь."""
        ...

    async def handle_event(self):
        """Обрабатывает событие из очереди."""
        ...

