import json
import re
import time
import fc
import base64
import save

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib.parse import quote
from loguru import logger
from bs4 import BeautifulSoup


class Scrape:
    def __init__(self, name, location, idOu):
        self.name = name
        self.location = location
        self.idOu = idOu

    def run(self):
        logger.info(f'start scrape location: {self.location}, name: {self.name}')

        data = []

        try:

            if self.name != '':
                url = f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={quote(self.name)}&ou={quote(self.location)}&univers=pagesblanches&idOu={self.idOu}"

                self.crwal(url, data)

            else:
                logger.error("Your link doesn't have a name!")
                exit(-1)
                # for a in fc.get_letters():
                #     url = f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={a}&ou={quote(self.location)}&univers=pagesblanches&idOu={self.idOu}"
                #     self.crwal(url, data)

        except Exception as e:
            print(e)

        if data:
            # 保存
            save.save_excel(data, self.name, self.location)
        else:
            logger.error("Didn't get any records")

    def crwal(self, url, data):
        """根据地点和名字开始爬取"""
        i = 1
        retry = 6  # 重试
        while 1:
            driver = fc.get_driver()

            time.sleep(10)
            page_url = f"{url}&page={i}"
            logger.info(f"Crwal: {page_url}")

            driver.get(page_url)

            try:
                WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#listResults ul.bi-list")))
                retry = 6
            except:
                status = self.check_page(driver)
                if status == 'end':
                    # 最后一页
                    logger.warning(f'Last page, End: {url}')
                    driver.close()
                    break

                # 其他错误重试5次
                if retry > 0:
                    retry -= 1
                    logger.error('Encounter an unexpect error, retry')
                    driver.close()
                    continue
                else:
                    logger.error(f'Something is wrong, please check Pagesjaunes')
                    exit(-1)

            soup = BeautifulSoup(driver.page_source, 'lxml')
            items = soup.select('li.bi')

            for item in items:
                # 姓名
                name = item.select_one('h3').text.strip()

                # 信息页路径
                try:
                    path_tmp = json.loads(item.select_one('.bi-denomination')['data-pjlb'])
                except:
                    continue

                path = base64.b64decode(path_tmp['url']).decode('ascii')

                if not self.filter(name, path):
                    continue

                # 找出多个电话
                phone_tmp = item.select_one('.bi-fantomas').text.replace(' ', '')
                phone_match = re.findall(r'(0\d{9})', phone_tmp)

                phone_nums = ''
                if len(phone_match) > 0:
                    phone_nums = ', '.join(phone_match)
                    # phone_nums = item.select_one('.number-contact').find(lambda span: len(span.attrs) == 0).text

                # 地址
                address_tmp = item.select_one('.bi-address > a').text
                address = address_tmp.split('\n')[1].replace('\xa0', ' ')

                print(f'Name: {name} - Phone: {phone_nums} - Address: {address}')

                data.append((name, phone_nums, address, ''))

            i += 1

            try:
                driver.close()
            except:
                pass

    def filter(self, name, path):
        """是否个人信息"""
        if len(name) <= 1:
            # 名字长度必须大于1
            return

        if path.startswith('/particuliers/'):
            # 只有 /particuliers/ 路径的页面才是个人
            return True

    def check_page(self, driver):
        """检查页面加载情况"""
        try:
            e = driver.find_element_by_class_name('pdr-msg')
            if e:
                if 'Cette personne ne souhaite peut-être pas paraître dans nos annuaires' in e.text:
                    # 超出页数范围
                    return 'end'
        except:
            return 'unexpect error'

