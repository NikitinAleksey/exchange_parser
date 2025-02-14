from app.controllers.bot_controller import BotController
from app.controllers.data_controller import DataController
from app.controllers.queue_controller import QueueController

__all__ = ["ControllerAggregator"]


class ControllerAggregator:
    bot = BotController
    data = DataController
    queue = QueueController
