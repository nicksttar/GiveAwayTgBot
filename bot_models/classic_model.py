from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramForbiddenError
from utils.states import Form_classic
from aiogram.fsm.context import FSMContext

from bot_models.classic_kb import kb_generation, give_kb, kb
from config import default_text, wellcome_text
from menu.mainkb import main_kb
from data.base_creation import DataBase

from main import bot

# Classic mode Router & db
db = DataBase()
router = Router()

# Routers FSM
@router.callback_query(F.data == 'pag:start:0')
async def fill_profile(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form_classic.for_who)
    await call.message.answer('Choose channel', reply_markup=kb())

@router.message(Form_classic.for_who, F.chat_shared)
async def next1(message: Message, state: FSMContext):
    await state.update_data(for_who=message.chat_shared.chat_id)
    await state.set_state(Form_classic.number_of)
    await message.answer('Number of participants', reply_markup=kb_generation(['10', '∞']))

@router.message(Form_classic.number_of)
async def next2(message: Message, state: FSMContext):
    if message.text.isdigit() or message.text == '∞':
        await state.update_data(number_of=message.text)
        await state.set_state(Form_classic.number_of_wins)
        await message.answer('Number of winners', reply_markup=kb_generation('1'))
    else: 
        await message.answer('Write a number!')

@router.message(Form_classic.number_of_wins)
async def next3(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(number_of_wins=message.text)
        await state.set_state(Form_classic.photo)
        await message.answer('Send photo', reply_markup=kb_generation('Default photo'))
    else:
        await message.answer('Write a number!')

@router.message(Form_classic.photo, F.photo)
async def next4(message: Message, state: FSMContext):
    photo_user = message.photo[-1].file_id
    await state.update_data(photo=photo_user)
    await state.set_state(Form_classic.short_description)
    await message.answer("Write short description", reply_markup=kb_generation('Default text'))

@router.message(Form_classic.photo, F.text == 'Default photo')
async def next5(message: Message, state: FSMContext):
    photo = FSInputFile("bot_models//give.jpg")
    await state.update_data(photo=photo)
    
    await state.set_state(Form_classic.short_description)
    await message.answer("Write short description", reply_markup=kb_generation('Defaul text'))

@router.message(Form_classic.short_description)
async def next6(message: Message, state: FSMContext):
    default = default_text
    if message.text == 'Default text':
        await state.update_data(short_description=default)
    else:
        await state.update_data(short_description=message.text)

    data = await state.get_data()


    number_of = data['number_of']
    number_wins = data['number_of_wins']

    await message.answer('Give created in your channel!', reply_markup=kb_generation(['Another give', 'Menu'], one_time=True))

    text_info = f"""🎁 <b>New Giveaway</b> 🎁

Participants: {number_of}
Winners: {number_wins}

Description: {data["short_description"]}"""
    try:
        await bot.send_photo(chat_id=data['for_who'], photo=data['photo'], caption=text_info, reply_markup=give_kb())
    except TelegramForbiddenError:
        await message.answer('Bot is not in Your channel or have no administrator permission.\n\nAdd bot into Your channel and make him admin to send gives!')
    await state.clear()

@router.message(F.text == 'Another give')
async def another_give(message: Message, state: FSMContext):
    await state.set_state(Form_classic.for_who)
    await message.answer('Choose channel', reply_markup=kb())

@router.message(F.text == 'Menu')
async def another_give(message: Message, state: FSMContext):
    await state.set_state(Form_classic.for_who)
    await message.answer(wellcome_text, reply_markup=main_kb.as_markup())

# Callback Data Join Btn
@router.callback_query(F.data == 'join')
async def next7(call: CallbackQuery, state: FSMContext):

    give_id = call.message.message_id


    new_data = call.message.caption.split('\n')

    number_of, number_wins = new_data[2:4]

    number_of = number_of.split(': ')[1]
    number_wins = int(number_wins.split(': ')[1])


    if number_of == '∞':
        number_of = 1000000


    db.create_db()
    db.insert_data(give_id=give_id, num_of=number_of, num_w=number_wins)

    nickname = call.from_user.username


    check = db.add_user(new_user=nickname, give_id=call.message.message_id)

    if check is True:
        await call.answer('Joined right now')
        
    elif check is False:
        await call.answer('You have already joined!')
        print(f'Give id: {call.message.message_id}')
    elif check == 'full':
        await call.answer('Now it is full!!!')



# Callback Data Start Btn        
@router.callback_query(F.data == '!start!')
async def launch(call: CallbackQuery):

    user = await bot.get_chat_member(chat_id=call.message.chat.id, user_id=call.from_user.id)


    if user.status in ['administrator', 'creator']:

        give_id = call.message.message_id
        res = db.start_give(give_id=give_id)

        if len(res) == 0:
            await call.answer('We have no one user to join in.')
        else:
            text = """Congratulations to: \n"""
            for i, j in enumerate(res, 1):
                temp = f'{i} @{j}\n'
                text += temp


            await call.message.delete()
            await call.message.answer('Giveaway is started!!!')
            await call.message.answer(text)
    else:

        await call.answer("You don't have admin rights.")
