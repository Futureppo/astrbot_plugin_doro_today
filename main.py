from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import At, Image, Plain
import os
import random

@register(
    "astrbot_plugin_doro_today",
    "Futureppo",
    "今天doro是什么结局？",
    "1.0.0",
    "https://github.com/your-repo/astrbot_plugin_doro_today"
)
class DoroTodayPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("dorotoday", alias={'今日doro', 'doro结局', 'dorotoday'})
    async def dorotoday(self, event: AstrMessageEvent):
        '''随机抽取一张doro结局并发送，同时@发送者'''
        # 获取发送者的ID和昵称
        sender_id = event.get_sender_id()
        try:
            sender_name = event.get_sender_name()
        except AttributeError:
            sender_name = str(sender_id)
        
        # 获取doro文件夹的路径
        doro_folder = os.path.join(os.path.dirname(__file__), "doro")
        
        # 检查doro文件夹是否存在
        if not os.path.exists(doro_folder):
            yield event.plain_result("doro文件夹不存在，请检查插件目录")
            return
        
        # 获取doro文件夹中的所有图片文件
        image_files = [f for f in os.listdir(doro_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        if not image_files:
            yield event.plain_result("doro文件夹中没有图片")
            return
        
        random_image = random.choice(image_files)
        image_path = os.path.join(doro_folder, random_image)
        image_name = os.path.splitext(random_image)[0]  # 去除文件扩展名
        
        message_chain = [
            At(qq=sender_id),
            Plain(f" 你今天的doro结局是：{image_name}"),
            Image.fromFileSystem(image_path)  
        ]
        
        # 发送消息
        yield event.chain_result(message_chain)