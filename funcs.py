import asyncio
from config import categories
from telebot import types

def create_inline_keyboard_buttons():
    button_list = []
    row = []
    max_buttons_per_row = 2

    for index, category in enumerate(categories):
        button = types.InlineKeyboardButton(f"{category}", callback_data=f'category_{index}')
        row.append(button)

        if len(row) == max_buttons_per_row or index == len(categories) - 1:
            button_list.append(row)
            row = []

    return button_list

