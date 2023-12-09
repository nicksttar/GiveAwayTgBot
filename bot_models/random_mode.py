import random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.states import Fast_Random
from aiogram.fsm.context import FSMContext

from bot_models.classic_kb import kb_generation

# Random mode Router
router = Router()


@router.callback_query(F.data == 'pag:start:1')
async def next1(call: CallbackQuery, state: FSMContext):
    await state.set_state(Fast_Random.number_of)
    await call.message.answer('Choose max number', reply_markup=kb_generation('1000'))

@router.message(Fast_Random.number_of)
async def next2(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(number_of=message.text)
        await state.set_state(Fast_Random.number_of_wins)
        await message.answer('Number of amount', reply_markup=kb_generation('1'))
    else:
        await message.answer('Write a number!')

@router.message(Fast_Random.number_of_wins)
async def next3(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(number_of_wins=message.text)
        data = await state.get_data()

        n_of = int(data['number_of'])
        n_wins = int(data['number_of_wins'])

        res = random.sample([i for i in range(0, n_of+1)], n_wins)
        res = ', '.join([str(i) for i in res])

        await message.answer(f'The number(s) is {res}', reply_markup=kb_generation(['Make more', 'Menu'], one_time=True))
        await state.clear()
    else:
        await message.answer('Write a number!')

@router.message(F.text == 'Make more')
async def make_more(message: Message, state: FSMContext):
    await state.set_state(Fast_Random.number_of)
    await message.answer('Choose max number', reply_markup=kb_generation('1000'))
