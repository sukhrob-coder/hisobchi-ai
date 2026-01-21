from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.filters.command import CommandObject
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.redis_utils import get_user_id_by_token, delete_linking_token
from app.models.transaction import Transaction, TransactionType, TariffType
from app.models.user import User

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandObject):
    token = command.args

    if not token:
        await message.answer(
            "Hisobchi.ai botiga xush kelibsiz!\n"
            "Iltimos, API orqali linking token oling va uni /start <token> ko‘rinishida yuboring."
        )
        return

    user_id = get_user_id_by_token(token)

    if not user_id:
        await message.answer("Noto‘g‘ri yoki muddati o‘tgan token.")
        return

    with SessionLocal() as db:
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            await message.answer("Foydalanuvchi topilmadi.")
            return

        user.telegram_id = str(message.from_user.id)
        user.chatID = str(message.chat.id)
        user.name = message.from_user.full_name
        db.commit()

    delete_linking_token(token)

    await message.answer(f"Muvaffaqiyatli bog‘landi! Xush kelibsiz, {user.name}!")


async def check_limit(user: User, db: Session) -> bool:
    if user.tariff == TariffType.PRO:
        return True

    now = datetime.now()
    month_start = datetime(now.year, now.month, 1)
    count = db.query(Transaction).filter(
        Transaction.user_id == user.id,
        Transaction.date >= month_start
    ).count()

    return count < 50


@router.message(Command("expense"))
async def cmd_expense(message: types.Message):
    await process_transaction(message, TransactionType.EXPENSE)


@router.message(Command("income"))
async def cmd_income(message: types.Message):
    await process_transaction(message, TransactionType.INCOME)


async def process_transaction(message: types.Message, t_type: TransactionType):
    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
        if not user:
            await message.answer("Sizning akkauntingiz hali bog'lanmagan. Iltimos, /start <token> yuboring.")
            return

        if not await check_limit(user, db):
            await message.answer("Sizning oylik limitungiz (50 ta transaction) tugagan. PRO tarifiga o'ting!")
            return

        parts = message.text.split(maxsplit=3)
        if len(parts) < 3:
            await message.answer(f"Format noto'g'ri. Misol: /{t_type} 50000 food nonushta")
            return

        try:
            amount = float(parts[1])
            category = parts[2]
            description = parts[3] if len(parts) > 3 else None

            transaction = Transaction(
                amount=amount,
                type=t_type,
                category=category,
                description=description,
                user_id=user.id
            )
            db.add(transaction)
            db.commit()

            await message.answer(f"✅ Saqlandi: {amount} ({category})")
        except ValueError:
            await message.answer("Miqdor (amount) raqam bo'lishi kerak.")
