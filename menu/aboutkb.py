from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, CallbackQuery

from config import about_text

# About Router & kb
router = Router()

about_kb = InlineKeyboardBuilder()
back_btn = InlineKeyboardButton(text='Back', callback_data='menu')

about_kb.add(back_btn)

@router.callback_query(F.data == 'about')
async def about(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(about_text, reply_markup=about_kb.as_markup())
