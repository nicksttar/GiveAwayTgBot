from aiogram.fsm.state import StatesGroup, State


class Form_classic(StatesGroup):
    """States for classic giveaway mode"""
    for_who = State()
    number_of = State()
    number_of_wins = State()
    photo = State()
    short_description = State()
    empty = State()


class Fast_Random(StatesGroup):
    """States for quick random mode"""
    number_of = State()
    number_of_wins = State()
    