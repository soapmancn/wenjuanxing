import os
import random
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth


async def question():
    PROXY_SERVER = os.environ['PROXY_SERVER']
    PROXY_USER = os.environ['PROXY_USER']
    PROXY_PASSWORD = os.environ['PROXY_PASSWORD']
    QUESTION_URL = os.environ['QUESTION_URL']
    TOTAL = int(os.environ['TOTAL_QUESTION'])

    while TOTAL > 0:
        try:
            browser = await launch({
                # 'headless': False,
                'timeout': 10000,
                'dumpio': True,
                'args': ['--no-sandbox',
                         '--window-size=1366,800',
                         '--disable-infobars',
                         '--proxy-server={}'.format(PROXY_SERVER)],
            })
            page = await browser.newPage()
            await page.setViewport({'width': 1366, 'height': 800})
            await stealth(page)
            if len(PROXY_USER) > 0:
                await page.authenticate({'username': PROXY_USER, 'password': PROXY_PASSWORD})
            sleepTime = random.randint(0, 1)

            await page.goto(QUESTION_URL)

            # 题目总数
            questionNum = await page.querySelectorAll('#fieldset1 > div.field.ui-field-contain')
            print('  第{}张问卷填写'.format(TOTAL))

            for item in questionNum:
                # 单选题
                radios = await item.querySelectorAll('.ui-radio')
                if len(radios) > 0:
                    radio = random.choice(radios)
                    while radios.index(radio) == len(radios)-1:
                        radio = random.choice(radios)
                    await radio.click()
                # 多选题
                checks = await item.querySelectorAll('.ui-checkbox')
                if len(checks) > 0:
                    checkTotal = len(checks)-1
                    # 随机一共选几个
                    needCheck = random.randint(1, checkTotal)
                    needList = random.sample(range(0, checkTotal), needCheck)
                    # 选择
                    for i in needList:
                        await checks[i].click()

            # 找到提交按钮提交
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
            await asyncio.sleep(4)
            TOTAL -= 1
            await browser.close()
        except Exception as e:
            print('  第{}张问卷异常'.format(TOTAL), e)
            await browser.close()

asyncio.get_event_loop().run_until_complete(question())
