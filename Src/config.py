import logging
import os

# путь к фалу Exel
script_dir = os.path.dirname(__file__)
PATH_FILE = os.path.join(script_dir, '../Data/operations.xlsx')

if not os.path.exists(PATH_FILE):
    print(f"Ошибка: файл {PATH_FILE} не найден!")

# тикеты биржи
sp500_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# настройки логирования
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")

os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)
