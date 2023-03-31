from pkg.plugin.host import EventContext, PluginHost
from pkg.plugin.models import *
from plugins.ChatPoeBot.pkg.config.poe_config import poe_config
from plugins.ChatPoeBot.pkg.mapper.poebots_mapper import bots
from plugins.ChatPoeBot.pkg.poe_bot import Poe, PoeBot

"""
在收到私聊或群聊消息"hello"时，回复"hello, <发送者id>!"或"hello, everyone!"
"""
help_msg = """!poe help 显示本帮助
!poe type <BotType> 切换机器人类型
BotType: Sage GPT4 Claude ClaudeInstant ChatGPT Dragonfly
其中GPT4与Claude,免费版每天只有一次对话机会
!poe purg [count] count为可选值，默认为回滚一次
!poe reset 重置对话
!poe history [count] count为可选值，默认返回最近5条历史
"""


@register(name="ChatPoeBot", description="与poe.com上的机器人对话", version="0.1", author="oliverkirk-sudo")
class HelloPlugin(Plugin):

    def __init__(self, plugin_host: PluginHost):
        self.poe_bot = PoeBot()
        self.bot_type = poe_config['default_bot_type']
        self.poe = Poe(self.poe_bot, self.bot_type).get_bot()
        pass

    @on(PersonNormalMessageReceived)
    @on(GroupNormalMessageReceived)
    def normal_message_received(self, event: EventContext, **kwargs):
        msg = kwargs['text_message']
        res_text, prefix = self.poe.chatWith(msg)
        if res_text:
            logging.debug("POE Started")
            event.add_return("reply", [prefix + res_text])
        else:
            logging.warning('未接收到返回消息，可能是对话次数已耗尽')
            event.add_return("reply", ['未接收到返回消息，可能是对话次数已耗尽'])
        event.prevent_default()
        event.prevent_postorder()

    @on(PersonCommandSent)
    @on(GroupCommandSent)
    def select_robot_type(self, event: EventContext, **kwargs):
        if kwargs['command'] == 'poe' and len(kwargs['params']):
            if kwargs['params'][0] == 'help':
                event.add_return("reply", [help_msg])
            elif kwargs['params'][0] == 'purg':
                if len(kwargs['params']) >= 2:
                    self.poe.purging_conversation(int(kwargs['params'][1]) * 2)
                else:
                    self.poe.purging_conversation()
                event.add_return("reply", ['已回滚对话（默认回滚一次）'])
            elif kwargs['params'][0] == 'reset':
                self.poe.clear_conversation()
                event.add_return("reply", ['已重置对话'])
            elif kwargs['params'][0] == 'history':
                history_text = ''
                index = 1
                if len(kwargs['params']) >= 2:
                    for i in self.poe.save_history(int(kwargs['params'][1])):
                        history_text += str(index) + '、' + i['node']['text'].replace('\n', '') + '\n'
                        index += 1
                else:
                    for i in self.poe.save_history():
                        history_text += str(index) + '、' + i['node']['text'].replace('\n', '') + '\n'
                        index += 1
                event.add_return("reply", [history_text])
            elif kwargs['is_admin'] and kwargs['params'][0] == 'type':
                if kwargs['params'][1] in bots.keys():
                    self.poe = Poe(self.poe_bot, bots[kwargs['params'][1]]).get_bot()
                    event.add_return("reply", [f'已切换到{kwargs["params"][1]}'])
                else:
                    event.add_return("reply", ['不正确的参数'])
        else:
            event.add_return("reply", ['不正确的参数'])
        event.prevent_default()
        pass

    def __del__(self):
        pass
