from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp

import aiohttp

BASE_URL = "https://api.thecatapi.com/v1/images/search"

@register("random_cat", "白星洛", "基于TheCatAPI的AstrBot随机猫图插件", "v1.0")
class RandomCarPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""


    # 注册指令的装饰器。
    @filter.command("随机猫图")
    async def random_cat(self, event: AstrMessageEvent):
        """随机猫图指令"""
        try:
            # 创建一个 aiohttp ClientSession 实例
            async with aiohttp.ClientSession() as session:
                # 发起 GET 请求
                async with session.get(BASE_URL) as response:
                    # 检查响应状态码
                    response.raise_for_status()
                    
                    # 解析 JSON 响应
                    data = await response.json()
                    # 获取图片 URL
                    image_url = data[0]['url']
                    logger.info(f"随机猫图 URL: {image_url}")
                    yield event.image_result(image_url)

        except aiohttp.ClientError as e:
            logger.error(f"请求错误: {e}")
            yield event.plain_result("请求猫咪图片失败，请稍后再试。")
        except Exception as e:
            logger.error(f"发生异常: {e}")
            yield event.plain_result("发生未知错误，请稍后再试。")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""