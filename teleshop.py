import asyncio
import aiohttp
import time
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from config import *
from language import *
from funcs import *
from sql_scripts import *

bot = AsyncTeleBot(token)


@bot.message_handler(commands=['start'])
async def start(message):
    user_id = message.chat.id
    if not user_exists(user_id):
        try:
            add_user(user_id)
        except Exception as e:
            print("Error {}".format(e))
    button_list1 = [
        types.InlineKeyboardButton(btn["catalog"], callback_data="btn_catalog"),
        types.InlineKeyboardButton(btn["shop_list"], callback_data="btn_shop_list"),
    ]
    button_list2 = [
        types.InlineKeyboardButton(btn["help"], callback_data="btn_help"),
    ]
    reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2])

    old_menu = check_start_menu_id(user_id)
    if old_menu:
        try:
            await bot.delete_message(message.chat.id, old_menu)
        except telebot.apihelper.ApiException:
            pass
    menu_message = await bot.send_message(message.chat.id, dct["start"], reply_markup=reply_markup)
    menu_id = menu_message.message_id
    add_start_menu_id(user_id, menu_id)


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    if call.data == "btn_catalog":
        button_list = create_inline_keyboard_buttons()
        back_button = types.InlineKeyboardButton(btn["back"], callback_data="btn_back_start")
        button_list.append([back_button])
        reply_markup = types.InlineKeyboardMarkup(button_list)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["catalog"], reply_markup=reply_markup)
    elif call.data.startswith('category_'):
        category_index = call.data.split('_')[1]
        category_name = categories[int(category_index)]

        await bot.answer_callback_query(call.id, f"Нажата категория: {category_name}")

        add_user_category(call.from_user.id, category_name)


        items = get_category_items(category_name)


        button_list = []
        for item in items:
            name = item[0]
            price = item[1]
            button = types.InlineKeyboardButton(f"{name} / {price}", callback_data=f"item_{category_index}_{name}")
            button_list.append([button])


        back_button = types.InlineKeyboardButton(btn["back"], callback_data="btn_back_category")
        button_list.append([back_button])

        reply_markup = types.InlineKeyboardMarkup(button_list)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["items"], reply_markup=reply_markup)

    elif call.data.startswith('item_'):
        item_name = call.data.split('_')[1:][1]
        category_name = check_user_category(call.from_user.id)
        category_index = 0
        for i in range(len(categories)):
            if categories[i] == category_name:
                category_index = i
                break
        item_info = get_item_info(category_name, item_name)
        item_code, item_name, item_description, item_price = item_info[0][0], item_info[0][1], item_info[0][2], item_info[0][3]

        await bot.answer_callback_query(call.id, f"Выбран элемент: {item_name} из категории {category_name}")

        item_photo_path = photo_path.format(item_code)

        button_list1 = [
            types.InlineKeyboardButton("Корзина", callback_data="btn_shop_list"),
        ]
        button_list2 = [
            types.InlineKeyboardButton(btn["back"], callback_data="btn_back_items")
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2])

        message_id = call.message.message_id
        await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        with open(item_photo_path, 'rb') as photo:
            await bot.send_photo(call.message.chat.id, photo)
        menu_message = await bot.send_message(chat_id=call.message.chat.id, text=f"{item_name} | {item_price}{currency}\n{item_description}",
                                    reply_markup=reply_markup)
        menu_id = menu_message.message_id
        user_id = call.message.chat.id
        add_start_menu_id(user_id, menu_id)


    elif call.data == "btn_back_start":
        button_list1 = [
            types.InlineKeyboardButton(btn["catalog"], callback_data="btn_catalog"),
            types.InlineKeyboardButton(btn["shop_list"], callback_data="btn_shop_list"),
        ]
        button_list2 = [
            types.InlineKeyboardButton(btn["help"], callback_data="btn_help"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["start"], reply_markup=reply_markup)

    elif call.data == "btn_back_category":
        button_list = create_inline_keyboard_buttons()
        back_button = types.InlineKeyboardButton(btn["back"], callback_data="btn_back_start")
        button_list.append([back_button])
        reply_markup = types.InlineKeyboardMarkup(button_list)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["catalog"], reply_markup=reply_markup)

    elif call.data == "btn_back_items":
        message_id = call.message.message_id
        await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id - 1)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        category_name = check_user_category(call.from_user.id)
        category_index = 0
        for i in range(len(categories)):
            if categories[i] == category_name:
                category_index == i
                break

        items = get_category_items(category_name)

        button_list = []
        for item in items:
            name = item[0]
            price = item[1]
            button = types.InlineKeyboardButton(f"{name} / {price}", callback_data=f"item_{category_index}_{name}")
            button_list.append([button])

        back_button = types.InlineKeyboardButton(btn["back"], callback_data="btn_back_category")
        button_list.append([back_button])

        reply_markup = types.InlineKeyboardMarkup(button_list)
        menu_message = await bot.send_message(chat_id=call.message.chat.id, text=dct["items"], reply_markup=reply_markup)
        menu_id = menu_message.message_id
        user_id = call.message.chat.id
        add_start_menu_id(user_id, menu_id)


async def main():
    while True:
        try:
            await bot.infinity_polling()
        except Exception as e:
            await print(f"⚠️ Bot has been crashed. Error: {str(e)}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()