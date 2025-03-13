from datetime import datetime, timedelta
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from gpt.generators import chat

router = Router()

class Generate(StatesGroup):
    text = State()

conversation_history = {}
last_interaction_time = {}

async def check_last_interaction(message: Message, state: FSMContext):
    user_id = message.from_user.id
    now = datetime.now()

    if user_id in last_interaction_time:
        last_message_time = last_interaction_time[user_id]
        if now - last_message_time > timedelta(minutes=5):
            await state.clear() 
            await message.answer("Здравствуй еще раз!")

    last_interaction_time[user_id] = now

@router.message(Command('start'))
async def run(message: Message, state: FSMContext):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    sticker_id = 'CAACAgIAAxkBAAIHHGbi2lVtVERahW57ZXfjQf9PhYUSAAI4CwACTuSZSzKxR9LZT4zQNgQ'
    await message.answer_sticker(sticker_id)
    await message.answer('Добро пожаловать в бот от компании ООО АСТРА! Введите свой запрос...')
    await state.clear()
    last_interaction_time[user_id] = datetime.now()  

@router.message(Command('contact'))
async def contact(message: Message):
    await message.answer("*Контакты для связи:*\nEmail:\no.zai@astra-st.com\nt.brm@astra-st.com\n\nТелефон:\n0700 107 005\n0700 107 013", parse_mode="Markdown")

@router.message(Command('about'))
async def about(message: Message):
    await message.answer(
        "*Каустическая сода высшего качества!* ⚡️\n\n"
        "Предлагаем вам уникальную возможность приобрести "
        "высококачественную каустическую соду от проверенного поставщика. 🏭\n\n"
    
        "💼 *Наша жидкая каустическая сода* — это средство для широкого применения! "
        "Благодаря выбору концентрации и удобной форме, она обеспечивает "
        "превосходную эффективность в промышленных процессах, включая:\n"
        "• Очистку 🧼\n"
        "• Обработку поверхностей 🛠\n"
        "• Производство различных химических веществ 🧪\n\n"
    
        "🔝 *Не упустите шанс улучшить производственные процессы* "
        "с нашей жидкой содой высшего качества! 🌟\n\n\n"
        
        "*Перекись водорода для максимальной эффективности!* 💧\n\n"
        "Мы предлагаем высококачественную перекись водорода для различных промышленных нужд. "
        "Наш продукт, производимый по строгим стандартам, обеспечивает надежность и чистоту, "
        "необходимые для эффективной работы вашего производства.\n\n"
        
        "💼 *Применение перекиси водорода*:\n"
        "• Дезинфекция и очистка\n"
        "• Производство химических веществ\n"
        "• Промышленные процессы, требующие высококачественного окислителя\n\n"
        
        "🔝 *Улучшите эффективность своего производства с нашей перекисью водорода* "
        "— продуктом высшей чистоты и надежности! 🌟\n\n\n"
        
        "*Высококачественная сетка МАК для ваших проектов!* 🔧\n\n"
        "Предлагаем сетку МАК, изготовленную по самым строгим стандартам из высококачественных материалов. "
        "Наши продукты подходят для широкого спектра применений: от строительства до сельскохозяйственных нужд.\n\n"
        
        "💼 *Особенности нашей сетки МАК*:\n"
        "• Прочность и долговечность\n"
        "• Гибкость в размерах под индивидуальный заказ\n"
        "• Надежность и устойчивость к внешним воздействиям\n\n"
        
        "🔝 *Улучшите свои проекты с нашей сеткой МАК* — надежной и долговечной! 🌟" , parse_mode="Markdown"
    )

@router.message(Command('site'))
async def site(message: Message):
    await message.answer('Наш сайт для посещения: https://ak-tash.kg/')

@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_message = message.text

    await check_last_interaction(message, state)

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_message})
    response = await chat(conversation_history[user_id])
    bot_response = response['choices'][0]['message']['content']
    conversation_history[user_id].append({"role": "assistant", "content": bot_response})

    await message.answer(bot_response)
    await state.clear()
