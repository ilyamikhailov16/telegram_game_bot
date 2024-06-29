from aiogram.types import BotCommand


command_list = [
    BotCommand(command='start', description='Начало игры'),
    BotCommand(command='replay', description='Перезагрузка игры'),
    BotCommand(command='help', description='Правила игры'),
    BotCommand(command='info', description='Информация о боте'),
]