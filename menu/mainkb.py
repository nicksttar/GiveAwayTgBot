from time import sleep

from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters.command import Command

from config import wellcome_text

# Main kb Router with launch and info btns
router = Router()


main_kb = InlineKeyboardBuilder()
main_btn1 = InlineKeyboardButton(text='How to use', callback_data='how')
main_btn2 = InlineKeyboardButton(text='Start Giveaway', callback_data='start_giveaway')
main_btn3 = InlineKeyboardButton(text='About', callback_data='about')

main_kb.row(main_btn1, main_btn2, main_btn3)
main_kb.adjust(1)


@router.message(Command('start'))
async def start(message: Message):
    await message.answer_dice(emoji='🎰')
    sleep(0.5)
    await message.answer(wellcome_text, reply_markup=main_kb.as_markup())

@router.callback_query(F.data == 'menu')
async def menu(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(wellcome_text, reply_markup=main_kb.as_markup())
    