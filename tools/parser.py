from settings import *

class Parser():#Thread):
    def __init__(self, profile_id: str, invisable=False) -> None:
        """Парсер с антидетект браузером Dolphin Anty

        Args:
            profile_id (str, optional): профиль ID от бразуера. Берется в самой программе, необходимо создать сперва ячейку под него
            invisable (bool, optional): запуск в свернутом режиме. Defaults to False.
            Версии эмуляторов: https://anty.dolphin.ru.com/docs/basic-automation/
            Для Linux сделать предвартилеьно chmo+x ..utils/cromedriver-linux
        """
        self.browser_startUp(profile_id,invisable = invisable)
        self.wait = WebDriverWait(self.driver,15)
        self.action = ActionChains(self.driver,1)
        
    def browser_startUp(self, PROFILE_ID,invisable):
        """Создание настройка и создания эмуляции браузера
        """ 
        options = webdriver.ChromeOptions()
        match platform.system():
            case "Windows":
                if platform.architecture() == "64bit":
                    chrome_drive_path = Service('/utils/chromedriver-win-x64')
                else: 
                    chrome_drive_path = Service('/utils/chromedriver-win-x86')
            case "Linux":
                chrome_drive_path = Service('./utils/chromedriver-linux')
                options.add_argument('--no-sandbox')
            case "Darwin":
                if platform.architecture() == "m1":
                    chrome_drive_path = Service('./utils/chromedriver-mac-m1')
                else:
                    chrome_drive_path = Service('./utils/chromedriver-mac-intel')


        response = requests.get(f'http://localhost:3001/v1.0/browser_profiles/{PROFILE_ID}/start?automation=1')
        respons_json = response.json()
        options.debugger_address = f"127.0.0.1:{respons_json['automation']['port']}"
        if invisable:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=chrome_drive_path,chrome_options=options)
    
    def element_count_greater_than(self,xpath, count):
        elements = self.driver.find_elements(By.XPATH, xpath)
        return len(elements) > count
    
    def _ya_scroll(self,xpath_locator:str,limit:int = int(config["Yandex"]["total_count"])):
        ad_elements_locator = (By.XPATH, xpath_locator)
        previous_ad_count = 0
        current_ad_count = len(self.driver.find_elements(*ad_elements_locator))
        while current_ad_count > previous_ad_count:
            scroll_track = self.driver.find_element(By.XPATH,"//div[@class='scroll__scrollbar-track']")
            previous_ad_count = current_ad_count
            actions = ActionChains(self.driver,duration=1000)
            time.sleep(2)

            x_coord = scroll_track.location['x'] + scroll_track.size['width']//2
            y_coord = scroll_track.location['y'] + scroll_track.size['height'] - 1
            actions.move_by_offset(x_coord,y_coord).perform()
            for _ in range(15):
                actions.click().perform()
                time.sleep(0.2)
            actions.move_by_offset(-x_coord,-y_coord).perform()
            actions.reset_actions()

            # Ожидание появления новых объявлений
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(self.driver.find_elements(*ad_elements_locator)) > previous_ad_count and len(self.driver.find_elements(*ad_elements_locator)) <= limit)
            except exceptions.TimeoutException:
                # Если новые объявления не загрузились, выходим из цикла
                break

            current_ad_count = len(self.driver.find_elements(*ad_elements_locator))

    def google_map(self,search_req,city,n):
        self.driver.get("https://yandex.ru/maps")
        time.sleep(1.5)
        
    def ya_map(self,search_req,city):
        """
        Сбор конкретно объявлений
        """
        import time
        self.driver.get("https://yandex.ru/maps")
        time.sleep(1.5)
        self.wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@class='input__control _bold']")))
        inp = self.driver.find_element(By.XPATH,"//input[@class='input__control _bold']")
        inp.send_keys(f"{search_req} в городе {city}")
        time.sleep(3)
        self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='popup _type_transparent _position_bottom _dropdown']")))
        inp.send_keys(Keys.ENTER)
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@data-object="search-list-item"]')))
        
        #Фильтр по рейтингу
        for button in self.driver.find_elements(By.XPATH,'//button[@type="button"]'):
            if  button.text.lower() == 'рейтинг':
                button.click()
                top_rait = self.driver.find_element(By.XPATH,'//div[@role="menuitemradio"]')
                self.wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@role="menuitemradio"]')))
                top_rait.click()
                break

        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//li[@class="search-snippet-view"]')))

        js_cursor = """
            var cursor = document.createElement('div');
            cursor.id = 'custom_cursor';
            cursor.style.position = 'absolute';
            cursor.style.zIndex = '9999';
            cursor.style.pointerEvents = 'none';
            cursor.style.width = '10px';
            cursor.style.height = '10px';
            cursor.style.border = '2px solid black';
            cursor.style.borderRadius = '50%';
            cursor.style.backgroundColor = 'red';
            document.body.appendChild(cursor);

            document.addEventListener('mousemove', function(e) {
            cursor.style.left = (e.pageX - 5) + 'px';
            cursor.style.top = (e.pageY - 5) + 'px';
            });
            """
        self.driver.execute_script(js_cursor)# курсор в браузере для тестирования*

        self._ya_scroll("//li[@class='search-snippet-view']")
        # Получение списка всех объявлений на странице
        
        ads_links = []
        for ad_element in self.driver.find_elements(By.XPATH,"//a[@class='search-snippet-view__link-overlay _focusable']"):
            link = ad_element.get_attribute("href")
            ads_links.append(f"{link}")
        self.ya_company_parsing(ads_links)

    def try_closing(self):
        self.driver.close()

    def ya_company_parsing(self,links):
        parse_data = []
        for link in links:
            data = self.collecting_company_card(link)
        parse_data.append(data) if data != None else None
        return(parse_data)

    def collecting_company_card(self,link):
        """
        Функция по сбору данных с одной карточки
        Разделитем для данных с некоторым количеством данных является "; " используйте его для обратной распаршивания массива данных(как картинки(photos) 
        или коменты(reviews) и расписания(working_time))
        Args:
            link (_type_): ссылка на саму компанию
        """
        self.driver.get(link)
        new_link = self.driver.current_url
        
        if 'discovery' in new_link:
            return None
        # Название
        try:
            title = self.driver.find_element(By.XPATH,'//*[@class="card-title-view__title-link"]').text
        except:
            title = self.driver.find_element(By.XPATH,'//*[@class="orgpage-header-view__header"]').text
        # Рейтинг(!!! единственный тип данных не str для переноса в БД)
        stars = float(self.driver.find_element(By.XPATH,'//div[@class="business-rating-badge-view__rating"]/span[2]').text.replace(",","."))
        # Данные из поделиться БОЛЬШЕ НЕТУ КНОПКИ
        # self.driver.find_element(By.XPATH,'//button[@aria-label="Поделиться"]').click()
        # self.wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="card-share-view"]//div[@class="card-feature-view__content"][1]')))
        # share_content = self.driver.find_elements(By.XPATH,'//div[@class="card-share-view"]//div[@class="card-feature-view__content"]')
        # share_link = share_content[1].text
        # coords = share_content[2].text

        share_link = self.driver.current_url
        coords = self.driver.current_url.split('/')[-1]
        # Адрес и город
        try:
            address = self.driver.find_element(By.XPATH,'//*[@class="orgpage-header-view__address"]//span[1]').text
            city = address.split(',')[-1]
        except:
            address = "None"
            city = "None"
        # Номер телефона
        try:
            phone_number = self.driver.find_element(By.XPATH,'//span[@itemprop="telephone"]').text
        except:
            phone_number = "None"
        # Сайт компании
        try:
            company_site = self.driver.find_element(By.XPATH,'//*[@class="business-urls-view__text"]').text
        except:
            company_site = "None"
        
        # График работы
        self.driver.find_element(By.XPATH,'//*[@class="business-card-working-status-view__main"]').click()
        working_time = list(map(lambda x: x.text, self.driver.find_elements(By.XPATH,'//*[@class="business-working-intervals-view__item"]')))
        working_time = '; '.join(working_time)
        # Соц сети
        try: 
            socials = list(map(lambda x: x.get_attribute('href'),self.driver.find_elements(By.XPATH,'//*[@class="business-contacts-view__social-button"]/a')))
            socials = '; '.join(socials)
        except:
            socials = "None"

        try:
            self.driver.get(f'{new_link[:new_link.rfind("/")]}/gallery{new_link[new_link.rfind("/"):]}')
            self.wait.until(EC.element_to_be_clickable((By.XPATH,'//img')))
            self._ya_scroll('//img',1000)
            photos = list(map(lambda x: x.get_attribute('src') ,self.driver.find_elements(By.XPATH,"//img")))
            photos = list(filter(lambda x: "yastatic" not in x,photos))
            photos = '; '.join(photos)
        except:
            photos = 'None'

        try:
            self.driver.get(f'{new_link[:new_link.rfind("/")]}/reviews{new_link[new_link.rfind("/"):]}')
            self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@class="business-review-view"]//div[@class="business-review-view__body"]')))
            self._ya_scroll('//*[@class="business-review-view"]//div[@class="business-review-view__body"]',10)
            reviews = list(map(lambda x: x.text ,self.driver.find_elements(By.XPATH,'//*[@class="business-review-view"]//div[@class="business-review-view__body"]')))[:10]
            reviews = '; '.join(reviews)
        except:
            reviews = 'None'
        
        try:
            self.driver.get(f'{new_link[:new_link.rfind("/")]}/features{new_link[new_link.rfind("/"):]}')
            descriptions = self.driver.find_element(By.XPATH,'//div[@class="business-features-view__valued-list"]').text
        except:
            descriptions = 'None'
        
        try: 
            tags = list(map(lambda x: x.text,self.driver.find_elements(By.XPATH,"//div[@class='features-cut-view']")))
            tags = "; ".join(tags)
        except:
            tags = None
        final_data = {
            "title":title,
            "stars":stars,
            "share_link":share_link,
            "address": address,
            "city": city,
            "map_link": new_link,
            "coords":coords,
            "descriptions": descriptions,
            "working_time":working_time,
            "phone_number":phone_number,
            "company_site":company_site,
            "socials":socials,
            "photos":photos,
            "reviews":reviews,
            "tags":tags
        }
        return(final_data)