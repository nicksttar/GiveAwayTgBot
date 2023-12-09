from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, CallbackQuery

from config import how_to_use_text

# how to use kb and Router
router = Router()

useit_kb = InlineKeyboardBuilder()
back_btn = InlineKeyboardButton(text='Back', callback_data='menu')

useit_kb.add(back_btn)

@router.callback_query(F.data == 'how')
async def about(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(how_to_use_text, reply_markup=useit_kb.as_markup())
    