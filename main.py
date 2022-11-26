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
    while TOTAL > 1:
        try:
            browser = await launch({
                # 'headless': False,
                # 'args': ['--no-sandbox', '--window-size=1366,850']
                'args': ['--no-sandbox', '--window-size=1366,850', '--proxy-server={}'.format(PROXY_SERVER)],
            })

            page = await browser.newPage()
            await page.setViewport({'width': 1366, 'height': 768})
            await stealth(page)
            await page.authenticate({'username': PROXY_USER, 'password': PROXY_PASSWORD})
            sleepTime = random.randint(0, 1)

            await page.goto(QUESTION_URL)

            # 题目总数 单选题type=3 多选题type=4
            questionNum = await page.querySelectorAll('#fieldset1 > div.field.ui-field-contain')
            totalNum = len(questionNum)
            print('总题数：{}'.format(totalNum))
            print('  还有{}张问卷待填'.format(TOTAL))

            for item in questionNum:
                print('    第{}题'.format(questionNum.index(item)+1))
                await asyncio.sleep(sleepTime)
                # 单选题
                radios = await item.querySelectorAll('.ui-radio')
                if len(radios) > 0:
                    radio = random.choice(radios)
                    while radios.index(radio) == len(radios)-1:
                        radio = random.choice(radios)
                    print('      单选题:{}'.format(radios.index(radio)))
                    await radio.click()
                # 多选题
                checks = await item.querySelectorAll('.ui-checkbox')
                if len(checks) > 0:
                    checkTotal = len(checks)-1
                    # 随机一共选几个
                    needCheck = random.randint(1, checkTotal)
                    needList = random.sample(range(0, checkTotal), needCheck)
                    print('      多选题:{}'.format(needList))
                    # 选择
                    for i in needList:
                        await checks[i].click()

            # 找到提交按钮提交
            await asyncio.sleep(sleepTime)
            submit = await page.querySelector('#ctlNext')
            await submit.click()

            # await asyncio.sleep(sleepTime)
            # # 智能检测确认
            # try:
            #     entry = await page.xpath('//*[@id="layui-layer1"]/div[3]/a[1]')
            #     await entry[0].click()
            # except Exception as e:
            #     print("智能检测确认", e)
            #
            # # 智能校验按钮
            # try:
            #     captcha = await page.querySelector('#captchaWrap')
            #     await captcha.click()
            # except Exception as e:
            #     print("智能校验按钮", e)

            # 页面延迟3s看是否提交成功
            await asyncio.sleep(3)
            await browser.close()
            TOTAL -= 1
            print('  还有{}张问卷待填'.format(TOTAL))
        except Exception as e:
            print('  第{}张问卷异常'.format(TOTAL), e)

asyncio.get_event_loop().run_until_complete(question())
