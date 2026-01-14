import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatJoinRequestHandler
)

# ⚠️ Obtenemos el token desde la variable de entorno
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ La variable de entorno TELEGRAM_TOKEN no está definida")

# Enlaces
RECOMMENDED_CHANNEL_TENNIS = "https://t.me/+PLuvmRoSXdIzZjg8"
RECOMMENDED_CHANNEL_BASKET = "https://t.me/+NPt2mDF_2UsyNzI0"
INSTAGRAM_LINK = "https://www.instagram.com/infapicks"

# Función para escapar caracteres especiales de MarkdownV2
def escape_md_v2_keep_bold(text: str) -> str:
    escape_chars = r'\_[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

# Mensaje base (SIN Instagram)
RAW_WELCOME_MESSAGE = (
    "🚨 *GRACIAS POR TU SOLICITUD PARA SEGUIR A INFA (HAY MUCHAS SOLICITUDES)*\n\n"
    "Mientras tanto, te recomiendo que te unas a los canales de la familia\n\n"
    "🎾 *INFA TENIS:* 👉 {link_tennis}\n"
    "⚽ *GAPUESTAS:* 👉 {link_basket}\n"
)

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user

    # 1️⃣ Reemplazamos links normales
    message_with_links = RAW_WELCOME_MESSAGE.format(
        link_tennis=RECOMMENDED_CHANNEL_TENNIS,
        link_basket=RECOMMENDED_CHANNEL_BASKET
    )

    # 2️⃣ Escapamos TODO el texto
    escaped_message = escape_md_v2_keep_bold(message_with_links)

    # 3️⃣ Añadimos Instagram (NO se escapa)
    escaped_message += (
        "\n📸 *INSTAGRAM:* 👉 [CLICK AQUI](" + INSTAGRAM_LINK + ")\n\n"
        "\\(Canales gestionados por expertos en cada deporte\\)"
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=escaped_message,
        parse_mode="MarkdownV2",
        disable_web_page_preview=True
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    print("🤖 bienvenido_acceso_bot activo (sin aprobar solicitudes)...")
    app.run_polling()

# ===== Servidor HTTP dummy para Render =====
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot activo!")

def run_dummy_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"🌐 Dummy web server corriendo en el puerto {port}")
    server.serve_forever()

# Iniciamos el servidor en un hilo paralelo
threading.Thread(target=run_dummy_server, daemon=True).start()

# Iniciamos el bot
if __name__ == "__main__":
    main()
