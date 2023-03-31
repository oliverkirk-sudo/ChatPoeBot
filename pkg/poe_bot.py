import logging
import random
import traceback

import poe
from plugins.ChatPoeBot.pkg.poe_bots_list import PoeBots

try:
    from plugins.ChatPoeBot.pkg.config.poe_config import poe_config
except Exception:
    logging.error('请配置poe_config.py')
    raise RuntimeError('请配置poe_config.py')

poe.logger.setLevel(logging.NOTSET)


class PoeBotAdapter:

    def __init__(self, client: poe.Client, poe_bots: PoeBots = poe_config['default_bot_type']):
        self.client = client
        self.bot = poe_bots.value
        self.bot_name = poe_bots.name

    def chatWith(self, msg: str):
        res_text = None
        try:
            for res_text in self.client.send_message(self.bot, msg):
                pass
            if res_text is None:
                logging.error('Poe出现错误')
        except RuntimeError as e:
            if e == 'Daily limit reached for beaver':
                logging.error(f'{self.bot}聊天次数达到上线')
        return res_text['text'] if res_text else None, '[POE]' + f'[{self.bot_name}]' if poe_config['prefix'] else ''

    def save_history(self, count=5):
        history = self.client.get_message_history(self.bot, count)
        if history:
            return history
        else:
            logging.warning('Poe保存历史失败')
            return None

    def purging_conversation(self, count: int = 2):
        self.client.purge_conversation(self.bot, count)
        logging.info(f'Poe回滚{count}条消息')

    def clear_conversation(self):
        self.client.send_chat_break(self.bot)


class PoeBot:
    def __init__(self):
        self.bot = []
        self.tokens = poe_config['tokens']
        self.proxy = poe_config['proxy'] if poe_config['proxy'] else None
        pass

    def login(self, token: str):
        client = None
        try:
            client = poe.Client(token, proxy=self.proxy)
        except ConnectionRefusedError:
            logging.error('连接失败，请检查网络和代理')
            traceback.print_exc()
        return client

    def check_token(self):
        if len(self.tokens) <= 0:
            logging.error('至少输入一个token')
        for token in self.tokens:
            self.bot.append(self.login(token))

    def get_bot(self):
        self.check_token()
        if len(self.bot) > 0:
            logging.info('获取到一个机器人')
            return self.bot[random.randint(0, len(self.bot) - 1)]
        else:
            logging.error('没有登录成功的机器人')


class Poe:
    def __init__(self, bots: PoeBot, bot_id: PoeBots):
        botClient = bots.get_bot()
        self.poe = PoeBotAdapter(botClient, bot_id)

    def get_bot(self):
        return self.poe
