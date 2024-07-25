import asyncio


from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
import random
import os
import sys
from common.commands import command_list
from common.cities import cities

bot = Bot(token="...")
dp = Dispatcher()

ALLOWED_UPDATES = ["message, edited_message"]
rules = "1) Каждый участник называет реально существующий в данный момент времени город любой страны, название которого начинается на ту букву, которой оканчивается название предыдущего города.\n2) Обычно исключения составляют названия, оканчивающиеся на твёрдый и мягкий знаки, а также букву «Ы» и «Ё»: в таких случаях участник называет город на предпоследнюю букву.\n3) Ранее названные города нельзя употреблять снова.\n4) Первый участник выбирает любой город.\n5) Во время игры запрещается пользоваться справочным материалом."


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Привет, бросишь мне вызов? Называй свой город")


@dp.message(Command("info"))
async def info_command(message: types.Message):
    await message.answer(
        "В моей базе более 7000 городов и муниципалитетов,\nэто немало, но отдельных городов, конечно, может не хватать,\nможешь написать на @ilyamikhailov16, если хочешь, чтобы был добавлен какой-то город"
    )


@dp.message(Command("replay"))
async def replay_command(message: types.Message):
    await message.answer("Перезапускаю бота...")
    os.execl(sys.executable, sys.executable, *sys.argv)


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(rules)


response = ""
used_cities_list = []
move_count = 0
unplayable_letters = "ыьъё"



@dp.message()
async def game(message: types.Message):
    global move_count
    global response

    if (
        message.text in cities
        and message.text not in used_cities_list
        and move_count == 0
    ):
        if message.text[-1] not in unplayable_letters:
            move_count += 1
            used_cities_list.append(message.text)
            response_variations = []
            for city in cities:
                if city not in used_cities_list:
                    if city[0] == message.text[-1].upper():
                        response_variations.append(city)
            response = random.choice(response_variations)
            used_cities_list.append(response)
            await message.answer(response)
        elif message.text[-1] in unplayable_letters:
            move_count += 1
            used_cities_list.append(message.text)
            response_variations = []
            for city in cities:
                if city not in used_cities_list:
                    if city[0] == message.text[-2].upper():
                        response_variations.append(city)
            response = random.choice(response_variations)
            used_cities_list.append(response)
            await message.answer(response)
    elif (
        message.text in cities
        and message.text not in used_cities_list
        and move_count > 0
    ):
        if (
            response[-1] not in unplayable_letters
            and message.text[0] == response[-1].upper()
            and message.text[-1] not in unplayable_letters
        ):
            used_cities_list.append(message.text)
            response_variations = []
            for city in cities:
                if city not in used_cities_list:
                    if city[0] == message.text[-1].upper():
                        response_variations.append(city)
            response = random.choice(response_variations)
            used_cities_list.append(response)
            await message.answer(response)
        elif (
            response[-1] not in unplayable_letters
            and message.text[0] == response[-1].upper()
            and message.text[-1] in unplayable_letters
        ):
            used_cities_list.append(message.text)
            response_variations = []
            for city in cities:
                if city not in used_cities_list:
                    if city[0] == message.text[-2].upper():
                        response_variations.append(city)
            response = random.choice(response_variations)
            used_cities_list.append(response)
            await message.answer(response)
        elif (
            response[-1] in unplayable_letters
            and message.text[0] == response[-2].upper()
            and message.text[-1] not in unplayable_letters
        ):
            used_cities_list.append(message.text)
            response_variations = []
            for city in cities:
                if city not in used_cities_list:
                    if city[0] == message.text[-1].upper():
                        response_variations.append(city)
            response = random.choice(response_variations)
            used_cities_list.append(response)
            await message.answer(response)
        elif (
            response[-1] in unplayable_letters
            and message.text[0] == response[-2].upper()
            and message.text[-1] in unplayable_letters
        ):
            used_cities_list.append(message.text)
            response_variations = []
            for city in cities:
                if city not in used_cities_list:
                    if city[0] == message.text[-2].upper():
                        response_variations.append(city)
            response = random.choice(response_variations)
            used_cities_list.append(response)
            await message.answer(response)
        else:
            await message.answer("Город не соответствует правилам")
    else:
        await message.answer("Я не знаю такого города или он уже был")
        await message.answer(
            "Возможно вы забыли дефис(можете попробовать убрать его)\nили допустили грамматическую ошибку"
        )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(
        commands=command_list, scope=types.BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
