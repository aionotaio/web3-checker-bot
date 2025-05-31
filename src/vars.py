import os


CLAIM_LINKS: dict[str, str] = {
    'sophon': 'https://claim.sophon.xyz/',
    'sxt': 'https://gigaclaim.spaceandtime.io/',
    '0g': 'https://claim.0gfoundation.ai/unlock',
    'jager': 'https://jager.meme/'
}

FORMATTED_NAMES: dict[str, str] = {
    'sophon': 'Sophon',
    'sxt': 'Space and Time',
    '0g': '0G',
    'jager': 'Jager (BNB memecoin)'
}

TICKERS: dict[str, str] = {
    'sophon': '$SOPH',
    'sxt': '$SXT',
    '0g': '$OG',
    'jager': '$JAGER'
}

TOKENS_PER_NODE_0G: int = 1143

PAGE_SIZE: int = 5

FULL_RESULTS_TEMP_CSV: str = 'temp_full_results.csv'
FULL_RESULTS_CSV: str = 'full_results.csv'
ELIGIBLE_RESULTS_TEMP_CSV: str = 'temp_eligible_results.csv'
ELIGIBLE_RESULTS_CSV: str = 'eligible_results.csv'

BOT_API_TOKEN: str = os.getenv('BOT_API_TOKEN', '')

RABBITMQ_HOST: str = os.getenv('RABBITMQ_HOST', '')
RABBITMQ_PORT: int = int(os.getenv('RABBITMQ_PORT', '5672'))
RABBITMQ_DEFAULT_USER: str = os.getenv('RABBITMQ_DEFAULT_USER', '')
RABBITMQ_DEFAULT_PASS: str = os.getenv('RABBITMQ_DEFAULT_PASS', '')

MONGO_HOST: str = os.getenv('MONGO_HOST', '')
MONGO_PORT: int = int(os.getenv('MONGO_PORT', '27017'))
MONGO_INITDB_ROOT_USERNAME: str = os.getenv('MONGO_INITDB_ROOT_USERNAME', '')
MONGO_INITDB_ROOT_PASSWORD: str = os.getenv('MONGO_INITDB_ROOT_PASSWORD', '')
