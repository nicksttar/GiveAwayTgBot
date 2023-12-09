from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, CallbackQuery

from config import modes_list

# Pagination Router 
router = Router()


class Paginator(CallbackData, prefix='pag'):
    action: str
    page: int

def paginator(page: int=0):
    builder = InlineKeyboardBuilder()
    start_btn = InlineKeyboardButton(text='Start', callback_data=Paginator(action='start', page=page).pack())
    b0 = InlineKeyboardButton(text='back', callback_data=Paginator(action='prev', page=page).pack())
    b1 = InlineKeyboardButton(text='menu', callback_data='menu')
    b2 = InlineKeyboardButton(text='next', callback_data=Paginator(action='next', page=page).pack())

    builder.add(start_btn)
    builder.row(b0, b1, b2)

    return builder.as_markup()

@router.callback_query(F.data == 'start_giveaway')
async def give(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(modes_list[0], reply_markup=paginator())



@router.callback_query(Paginator.filter(F.action.in_(['prev', 'next'])))
async def testt(call: CallbackQuery, callback_data: Paginator):
    page_num = int(callback_data.page)


    if callback_data.action == 'prev':
        page = page_num-1 if page_num > 0 else 0

    elif callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(modes_list)-1) else page_num
        
    try:
        await call.message.edit_text(f"{modes_list[page]}", reply_markup=paginator(page=page))
    except Exception:
        print('NO')
