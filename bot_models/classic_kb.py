from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, KeyboardButtonRequestChat

# kb generator
def kb_generation(text: str | list, one_time=False) -> ReplyKeyboardBuilder:
    if isinstance(text, str):
        text = [text]

    builder = ReplyKeyboardBuilder()

    [builder.add(KeyboardButton(text=btn)) for btn in text]


    return builder.as_markup(resize_keyboard=True, one_time_keyboard=one_time)

# Need to remove kb
rmk = ReplyKeyboardRemove()

# In give message kb
def give_kb():  
    kb = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='Join', callback_data='join')
    btn2 = InlineKeyboardButton(text='Start', callback_data='!start!')
    kb.add(btn2)
    kb.add(btn1)
    kb.adjust(1)

    return kb.as_markup()

# Chat request kb
def kb():
    kb = ReplyKeyboardBuilder()
    b_test = KeyboardButton(
        text='Channels',
        request_chat=KeyboardButtonRequestChat(
            request_id=1,
            chat_is_channel=True,
            chat_is_forum=True,
            chat_has_username=True,
            chat_is_created=True,
        )
    )
    kb.add(b_test)

    return kb.as_markup(resize_keyboard=True)
