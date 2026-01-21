# Hisobchi.ai - Simplified Backend & Telegram Bot

Hisobchi.ai is a fintech product that allows users to track their income and expenses via a Telegram bot and REST API, with tariff-based limits and analysis.

## 🚀 Features
- **Authentication**: JWT-based registration and login via REST API.
- **Telegram Bot Integration**: Token-based user linking and transaction recording.
- **Tariff Limits**:
    - **FREE**: 50 transactions per month, monthly summary.
    - **PRO**: Unlimited transactions, flexible summaries (daily, monthly, custom range).
- **Reports**: Aggregate income, expense, and balance via API and Bot.

## 🛠 Tech Stack
- **Backend**: FastAPI
- **Database**: SQLAlchemy + PostgreSQL
- **Cache/Memory**: Redis (for linking tokens)
- **Telegram Bot**: Aiogram 3.x
- **Security**: Passlib (bcrypt), PyJWT

## 🏁 Getting Started

### 1. Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/hisobchi
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=1
BOT_TOKEN=your_telegram_bot_token
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the API
```bash
uvicorn app.main:app --reload
```

### 4. Run the Telegram Bot
```bash
python bot_main.py
```

## 🔄 User Linking Explanation
1. User registers via `POST /auth/register`.
2. User logs in via `POST /auth/login` to get a JWT token.
3. User requests a linking token via `GET /auth/linking-token` (requires JWT).
4. User sends `/start <token>` to the Telegram bot.
5. The bot validates the token in Redis, associates the user's `telegram_id` with their API `user_id`, and saves the context.

## 🧠 Q&A (Technical Questions)

**1. FREE user 51-transaction yuborsa nima bo‘ladi?**
Bot foydalanuvchiga limit tugaganligini va PRO tarifiga o'tishni tavsiya qiluvchi xabar qaytaradi. API esa mos ravishda xatolik qaytarishi kerak (masalan, 403 Forbidden yoki 429 Too Many Requests, mantiqan 403 to'g'riroq agar bu biznes limit bo'lsa).

**2. Telegram’dan parallel requestlar qanday muammo keltirishi mumkin?**
Parallel requestlar "Race Condition" muammosini keltirib chiqarishi mumkin. Masalan, foydalanuvchi bir vaqtning o'zida ikkita transaction yuborsa, limit tekshiruvi ikkalasida ham o'tib ketishi va natijada foydalanuvchi limitdan ko'proq transaction yuborishi mumkin. Buni oldini olish uchun Redis lock'laridan yoki DB darajasidagi tranzaksiyalardan foydalanish kerak.

**3. Tokenni Telegram orqali yuborish qanchalik xavfsiz?**
Bu o'rtacha xavfsiz, lekin mukammal emas. Telegram kanali shifrlangan bo'lsa-da, token xabar sifatida ko'rinadi. Xavfsizlikni oshirish uchun tokenni juda qisqa vaqt (masalan, 5 daqiqa) amalda bo'lishini ta'minlash va bir marta ishlatilgandan keyin o'chirish lozim.

**4. Production’da Telegram botni qanday scale qilardingiz?**
Botni scale qilishda `Webhook` rejimidan foydalanish tavsiya etiladi. Bir nechta bot instance'larini load balancer orqasiga qo'yish va ularni Redis orqali muvofiqlashtirish (Dispatcher storage) mumkin. Shuningdek, og'ir vazifalarni (masalan, hisobot tayyorlash) Celery kabi worker'larga yuklash kerak.

**5. Agar vaqt bo‘lsa, nimani yaxshilardingiz?**
- **Alembic**: Ma'lumotlar bazasi migratsiyalarini boshqarish uchun.
- **Docker**: Loyihani oson deploy qilish uchun.
- **Tests**: Pytest orqali unit va integration testlar.
- **Logging/Sentry**: Xatoliklarni kuzatib borish uchun.
- **FSM (Finite State Machine)**: Botda foydalanuvchi bilan muloqotni murakkabroq qilish uchun (masalan, transactionni qadam-baqadam kiritish).
