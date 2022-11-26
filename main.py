import asyncio
import random
from pyppeteer import launch
from pyppeteer_stealth import stealth


async def main():
    # 需要的问卷数量
    num = 10
    while num != 0:
        print(num)
        await question()
        num -= 1


async def question():
    # launch方法会新建一个browser对象,然后赋值给browser
    browser = await launch({
        # 路径就是你的谷歌浏览器的安装路径
        # 'executablePath': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        # Pyppeteer 默认使用的是无头浏览器,所以要显示需要给False
        'headless': False,
        # 设置Windows-size和Viewport大小来实现网页完整显示 proxy-server 代理IP服务
        'args': ['--no-sandbox', '--window-size=1366,850', '--proxy-server=tunnel3.qg.net:16997'],
    })

    # 调用 newPage 方法相当于浏览器中新建了一个选项卡,同时新建了一个Page对象
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    # 防止页面识别出脚本(反爬虫关键语句)
    await stealth(page)
    # 设置代理IP
    await page.authenticate({'username': 'EFE0EADG', 'password': '503CCC2E26CG'})
    # 设置随机休眠
    sleepTime = random.randint(1, 3)

    # 调用了Page对象的goto方法就相当于在浏览器中输入问卷的网址,浏览器跳转到了对应的页面进行加载
    await page.goto('https://www.wjx.cn/vm/mB2XPLL.aspx')
    # 填空题：page.type(selector,text),在指定selector的元素上填写text
    # await page.type('#q1', '姓名')
    # await page.type('#q2', '学号')
    # await page.type('#divquestion5 > table > tbody > tr:nth-child(1) > td > div > textarea', '体温')

    # 单选题：先用page.querySelector(selector)找到指定的元素,再调用元素的click()方法
    # button = await page.querySelector("#divquestion3 > ul > li:nth-child(8)")
    await asyncio.sleep(sleepTime)
    radioList = await page.querySelectorAll('#div1 > div.ui-controlgroup.column1 > div.ui-radio')
    radio = random.choice(radioList)
    await radio.click()
    await asyncio.sleep(sleepTime)
    radioList = await page.querySelectorAll('#div2 > div.ui-controlgroup.column1 > div.ui-radio')
    radio = random.choice(radioList)
    await radio.click()

    # 地址题：先点击手动填写地址,再在地址框内填写相应地址
    # address = await page.querySelector("#divquestion7 > ul > li:nth-child(1) > label")
    # await address.click()
    # await page.type('#q9', '地址')

    # 日期选择题：先点击日期选择框,在出现的iframe寻找元素并调用click()方法
    # date1 = await page.querySelector("#q4")
    # await date1.click()

    # frame = page.frames
    # date2 = await frame[1].querySelector('#selectTodayButton')
    # await date2.click()

    # 找到提交按钮提交
    await asyncio.sleep(sleepTime)
    submit = await page.querySelector('#ctlNext')
    await submit.click()

    await asyncio.sleep(sleepTime)
    # 智能检测确认
    try:
        entry = await page.xpath('//*[@id="layui-layer1"]/div[3]/a[1]')
        await entry[0].click()
    except Exception as e:
        print("智能检测确认", e)

    # 智能校验按钮
    try:
        captcha = await page.querySelector('#captchaWrap')
        await captcha.click()
    except Exception as e:
        print("智能校验按钮", e)

    # 页面延迟3s看是否提交成功
    await asyncio.sleep(3)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
