"""Module for Telegram Bot."""
import asyncio
import logging
import sys
from os import getenv

import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv


load_dotenv()
USER_TOKEN = getenv('USER_TOKEN')
bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher()
headers = {
    'User-Agent': 'Bot User Agent',
    'Authorization': f'Token {USER_TOKEN}',
}


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    """
    Handle the /start command.

    Send initial buttons or options to the user to start the bot.

    Args:
        message (types.Message): The message object that contains the
            details of the command sent by the user.
    """
    await send_initial_buttons(message)


async def send_initial_buttons(message_or_callback):
    """
    Send initial buttons to the user based on data fetched from API.

    Args:
        message_or_callback (Union[types.Message, types.CallbackQuery]):
        The incoming message or callback query from the user.
    """
    builder = InlineKeyboardBuilder()

    response = requests.get(
        'http://host.docker.internal:8000/api/masters/',
        headers=headers,
        timeout=1,
    )
    if response.status_code == 200:
        buttons_data = response.json()
        for button in buttons_data:
            button_id = button.get('id')
            button_title = button.get('title')
            builder.row(types.InlineKeyboardButton(
                text=button_title, callback_data=f'btn:{button_id}'),
            )
        builder.row(types.InlineKeyboardButton(
            text='НАЗАД', callback_data='btn:back'),
        )
        if isinstance(message_or_callback, types.Message):
            await message_or_callback.answer('Выберите кнопку:',
                                             reply_markup=builder.as_markup())
        elif isinstance(message_or_callback, types.CallbackQuery):
            await message_or_callback.message.answer(
                'Выберите кнопку:',
                reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith('btn'))
async def handle_button(callback: types.CallbackQuery):
    """
    Handle button presses for the bot's inline keyboard.

    Args:
        callback (types.CallbackQuery): Object containing button press data.

    Processes button presses, displays descriptions and buttons fetched from
    an API. If 'back' button pressed, sends initial buttons.
    """
    btn_ids = callback.data.split(':')[1:]
    if 'back' in btn_ids:
        await send_initial_buttons(callback)
        return

    logging.info(btn_ids)

    response = requests.get(
        'http://host.docker.internal:8000/api/masters/',
        headers=headers,
        timeout=1,
    )
    if response.status_code != 200:
        await callback.message.answer('Не удалось получить список кнопок.')
        return

    btn = None
    child_btns = response.json()
    for btn_id in btn_ids:
        btn = get_btn_by_id(btn_id, child_btns)
        if btn is None:
            await callback.message.answer('Кнопка не найдена.')
            return
        child_btns = btn.get('buttons', [])

    description = btn.get('description', '') if btn else ''
    if description:
        await callback.message.answer(description, parse_mode='markdown')

    if child_btns:
        builder = InlineKeyboardBuilder()
        for child_btn in child_btns:
            button_id = child_btn.get('id')
            button_title = child_btn.get('title')
            builder.row(types.InlineKeyboardButton(
                text=button_title,
                callback_data=f'{callback.data}:{button_id}'),
            )
        builder.row(types.InlineKeyboardButton(
            text='НАЗАД', callback_data='btn:back'),
        )
        await callback.message.answer('Выберите кнопку:',
                                      reply_markup=builder.as_markup())
    elif not description:
        await callback.message.answer('Описание отсутствует.')


def get_btn_by_id(btn_id, data):
    """
    Retrieve a button from a list of button data based on its ID.

    Args:
        btn_id (int): The ID of the button to retrieve.
        data (list): List of dictionaries containing button data.

    Returns:
        dict or None: If a button with the specified ID is found, returns
        the dictionary representing that button. Otherwise, returns None.
    """
    for btn_dct in data:
        btn_full_id = btn_dct.get('id')
        if int(btn_full_id) == int(btn_id):
            logging.info(f'{btn_full_id} / id: {btn_id}')
            return btn_dct
    return None


async def main():
    """
    Start polling the bot.

    Sets up logging, configures logging level to INFO.
    Initiates bot polling to start receiving updates.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
