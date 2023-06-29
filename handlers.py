from aiogram import types, F, Router
from aiogram.types import Message, callback_query
from aiogram.filters import Command
from aiogram import flags
from aiogram.fsm.context import FSMContext

import kb
import text

import utils
from states import Gen

router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
@router.message(F.text == "️️️️️️️️️️️◀️Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)
# @router.message()
# async def message_handler(msg: Message):
#     await msg.answer(f'Твой АйДи: {msg.from_user.id}')
@router.callback_query(F.data == "generate_text")
async def input_text_prompt(clbck: callback_query.CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text(text.gen_text)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)

@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    res = await utils.generate_text(prompt)
    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.edit_text(res[0] + text.text_watermark, disable_web_page_preview=True)

@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: callback_query.CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_prompt)
    await clbck.message.edit_text(text.gen_image)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)

@router.message(Gen.img_prompt)
@flags.chat_action("upload_photo")
async def generate_image(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    img_res = await utils.generate_image(prompt)
    if len(img_res) == 0:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.delete()
    await mesg.answer_photo(photo=img_res[0], caption=text.img_watermark)