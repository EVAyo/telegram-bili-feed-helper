import pytest


@pytest.mark.asyncio
async def test_dynamic_parser():
    from biliparser import biliparser
    from database import db_init

    await db_init()
    urls = [
        "https://t.bilibili.com/379593676394065939?tab=2",  # 动态带图非转发
        "https://t.bilibili.com/371426091702577219?tab=2",  # 引用带视频
        "https://t.bilibili.com/371425692269567902?tab=2",
        "https://t.bilibili.com/371422853294071821?tab=2",
        "https://t.bilibili.com/371416015710288135?tab=2",
        "https://t.bilibili.com/362547324854991876",  # 音频（带动态）
        "https://t.bilibili.com/368023506944203045",  # 投票
        "https://t.bilibili.com/366460460970724962",  # 引用投票
        "https://t.bilibili.com/371409908269898061",  # 文章（带动态）
        "https://t.bilibili.com/371040919035666819",  # 小视频（动态）
        "https://t.bilibili.com/371050565530180880?tab=2",  # 引用小视频
        "https://b23.tv/xZCcov",  # 引用带图
        "https://t.bilibili.com/h5/dynamic/detail/371333904522848558",  # 文章（不带动态）
        "https://www.bilibili.com/audio/au1360511",  # 音频
        "https://live.bilibili.com/115?visit_id=7zr5hnihuiw0",  # 直播
        "https://www.bilibili.com/video/BV1g64y1u7RT",  # 视频
        "https://www.bilibili.com/bangumi/play/ep317535",  # 番剧集
        "https://www.bilibili.com/bangumi/play/ss33055",  # 番剧季
        "https://t.bilibili.com/687612573189668866",  # 预约动态
    ]
    for i in urls:
        result = await biliparser(i)
        assert result
