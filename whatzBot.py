from selenium.webdriver.chrome.webdriver import WebDriver
import pyautogui
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ChromeOptions

class WhatzBot:
    __elementsFound = []  # elements found
    __url = 'https://www.whatsapp.com/'  # the url for whatsapp
    __urlToSendMessages = 'https://web.whatsapp.com/send?phone='  # url for whatsupp also to send messages to spesfic phone
    __messageBox = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
    __sendingMessage = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'  # the xpath file for sending the message
    __attachmentIcon = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
    __addButton = '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[1]/button'
    __sendButton = '/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div'
    __picture_box = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input'
    __document_box = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[4]/button/input'
    __photosList = []
    __text_message = ''
    __is_there_pic = False
    __is_there_doc = False
    __driver: WebDriver = None

    def __init__(self, photolist='', document_list='', textmessage='', path='chromedriver.exe'):
        self.__photosList = photolist
        self.__document_list = document_list
        self.__text_message = ''
        self.__driver = webdriver.Chrome(path)


    def set_text_message(self, textmessage):
        self.__text_message = ''
        print(self.__text_message)

    def set_photo_list(self, photolist):
        self.__photosList = photolist
        if photolist != []:
            self.__is_there_pic = True

    def set_document_list(self, document_list):
        self.__document_list = document_list
        if len(document_list) >= 1:
            self.__is_there_doc = True

    def get_driver(self) -> WebDriver:
        return self.__driver

    def startingWhats(self):
        # in this function we get the whatsapp webpage and wait for one second then we click on the one that gets us to the web whatsapp
        # then we wait for the user to scan the barcode
        self.__driver.get(self.__url)
        while True:  # while true
            sleep(1)  # sleep for one second so we can wait and load for the page to open
            self.__driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[1]/header/div/div[2]/span[1]/a[1]/h5').click()  # head for entering whatsapp page
            sleep(1)
            try:
                self.__driver.find_element_by_xpath('//*[@id="content-wrapper"]/div[1]/div/a')
            except NoSuchElementException:
                break
        X = True
        while X:
            try:
                self.__driver.find_element_by_xpath('//*[@id="side"]/header/div[2]/div/span/div[2]/div/span')
                X = False
            except NoSuchElementException:
                sleep(1)
                print("here 2")

    def contactingNumbers(self, phoneNumber, index=0):
        print(phoneNumber)
        X = True
        countX = 0
        bool = False
        try:
            print("___________")
            self.urlPlusNum = self.__urlToSendMessages + '966' + phoneNumber
            self.__driver.get(self.urlPlusNum)
            print(self.__driver.switch_to.alert.text)
            self.__driver.switch_to.alert.accept()
            self.__driver.switch_to.alert.dismiss()
        except:
            pass
        while X:
            if countX > 30:  # if it takes more than 30countX units re enter the link
                self.urlPlusNum = self.__urlToSendMessages + '966' + phoneNumber
                self.__driver.get(self.urlPlusNum)
                countX = 0
                sleep(0.5)
            try:
                sleep(0.4)
                self.__send_message()
            except NoSuchElementException:  # if the page of the user did not show up then incremint the countX time unit by one
                countX += 1
                print("no such element")
                try:  # if the number does not exist we are gonna return true
                    num_not_found = self.__driver.find_element_by_xpath('/html/body/div[1]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[1]').text
                    print(num_not_found)
                    if num_not_found == 'Phone number shared via url is invalid.' or num_not_found == 'إن رقم الهاتف الذي تمت مشاركته عبر الرابط غير صحيح.':
                        return True
                    else:
                        sleep(0.5)
                        continue
                except NoSuchElementException:  # the number exists so we have to wait by 0.4 seconds
                    sleep(0.4)
                    continue
                except StaleElementReferenceException:
                    sleep(0.5)
                    continue
            except UnexpectedAlertPresentException:
                return False
            if self.__is_there_pic:
                for i in self.__photosList:
                    self.__send_photo(i)
            if self.__is_there_doc:
                self.__send_document()
                sleep(1)
            self.is_sent()
            return True

    def __send_document(self):
        for i in self.__document_list:
            while True:
                try:
                    self.__driver.find_element_by_xpath(self.__attachmentIcon).click()
                    document_box = self.__driver.find_element_by_xpath(self.__document_box)
                    document_box.send_keys(i)
                    sleep(0.5)
                    break
                except NoSuchElementException:
                    continue
                except WebDriverException:
                    sleep(0.4)
                    continue
            while True:
                try:
                    self.__driver.find_element_by_xpath(self.__sendButton).click()
                    sleep(0.5)
                    break
                except NoSuchElementException:
                    continue
                except ElementClickInterceptedException:
                    continue

    def __send_message(self):
        self.__driver.find_element_by_xpath(self.__messageBox).send_keys(self.__text_message)
        self.__driver.find_element_by_xpath(self.__sendingMessage)

    def __send_photo(self, i):
        while True:
            try:
                self.__driver.find_element_by_xpath(self.__attachmentIcon).click()
                pictureBox = self.__driver.find_element_by_xpath(self.__picture_box)
                pictureBox.send_keys(i)
                sleep(1)
                break
            except NoSuchElementException:
                print("The problem from puting picutre twice is here")
                continue
            except WebDriverException:
                print('fuck you and your fucking problem')
                sleep(0.3)
                continue
        while True:
            try:
                self.__driver.find_element_by_xpath(self.__sendButton).click()
                sleep(0.3)
                break
            except NoSuchElementException:
                print("The problem from puting picutre twice is here 2")
                continue
            except ElementClickInterceptedException:
                continue

    def is_sent(self):
        count = 0
        the_text = self._last_messages()
        the_message_status_element = '/div/div/div/div[2]/div/div/span'
        while count < 10:
            try:
                is_message_sent = self.__driver.find_element_by_xpath(
                    the_text + the_message_status_element)
                inc = 0
                while is_message_sent.get_attribute("aria-label") != '  تم تسليمها  ' and is_message_sent.get_attribute(
                        "aria-label") != '  تمت قراءتها  ' and inc < 3:
                    print("hello")
                    sleep(1)
                    inc += 1
                break
            except NoSuchElementException:
                sleep(0.3)
                print("there is clearly an error")
                count += 1
                continue
        return

    def _last_messages(self, last_or_all=True):
        count = 2
        count_error = 0
        list_of_elements = []
        num_1_2 = '3'
        try:
            self.__driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/div[3]/div/div[2]/div[4]')
        except NoSuchElementException:
            num_1_2 = '2'
        while True:
            try:
                the_text = '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/div[3]/div/div[2]/div[' + num_1_2 + ']/div[' + str(
                    count + 1) + ']'
                print(the_text)
                print("hello")
                s = self.__driver.find_element_by_xpath(the_text)
                print("hello")
                print(s.text)
                count += 1
                list_of_elements.append(the_text)
            except NoSuchElementException:
                if count_error > 10:
                    break
                print("error")
                count_error += 1
        if last_or_all:
            print(list_of_elements)
            return list_of_elements[-1]
        else:
            return [self.__driver.find_element_by_xpath(element).text for element in list_of_elements]
