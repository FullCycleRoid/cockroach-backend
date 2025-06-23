from telegram import Bot
from telegram.error import TelegramError

from src.config import settings


async def send_telegram_message(chat_id: str, message: str):
    try:
        bot = Bot(token=settings.telegram_token)
        await bot.send_message(chat_id=chat_id, text=message)
        return True
    except TelegramError as e:
        print(f"Telegram error: {e}")
        return False


async def send_invite_notification(player_id: str, game_id: str, creator_username: str):
    message = (
        f"🎮 Вы приглашены в игру 'Тараканы'!\n"
        f"👤 Создатель: @{creator_username}\n"
        f"👉 Присоединяйтесь: https://your-domain.com/game/{game_id}"
    )
    return await send_telegram_message(player_id, message)
