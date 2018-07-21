#!/usr/bin/python
# -*- coding: utf-8  -*-

# dependency for Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Dependency for wait element
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException,
                                        TimeoutException,
                                        StaleElementReferenceException,
                                        ElementNotInteractableException,
                                        SessionNotCreatedException)

# other element
from utils import *
from detect_image import *

# Dependancy for other element
import urllib
import time
import pickle
import string
import os
from PIL import Image
import sys
import re
import concurrent.futures
from bs4 import BeautifulSoup
import yaml
import platform

# define color for print
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNYELLOW = '\033[1;33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Read YML file
with open("config.yml", 'r') as stream:
    data_loaded = yaml.load(stream)


# Cookie saver
def save_cookies(driver, file_path):
    LINE = "{domain} False {path} {secure} {expiry} {name} {value}\n"
    with open(file_path, 'w') as file:
        for cookie in driver.get_cookies():
            file.write(LINE.format(**cookie))


def load_cookies(driver, file_path):
    with open(file_path, 'r') as file:
        driver.execute_script(file.read())


# compare two image
def image_diff(i1, i2):
    i1 = Image.open(i1)
    i2 = Image.open(i2)
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."

    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents


# check percent of two image
def check_images(image1, image2):
    pourcent = image_diff(image1, image2)
    # print(pourcent)
    if pourcent <= 0.19:
        return True
    else:
        return False



class PoleEmplois():
    '''
    Initalisation account on pole emploi and define the broswer
    option for navigate on the page.
    '''
    def __init__(self, compte, password):
        ___author___ = "vBlackOut"
        ___version___ = "1.0.5c (Beta)"

        print('''{}
-----------------------------------------------------------------------------
{}  _ \    _ \    |      __|    __|    \  |   _ \   |       _ \   _ _| {}
{}  __/   (   |   |      _|     _|    |\/ |   __/   |      (   |    |  {}
{} _|    \___/   ____|  ___|   ___|  _|  _|  _|    ____|  \___/   ___| {}
-----------------------------------------------------------------------------{}

Author: {}{:>15}{}
Version: {}{:>18}{}
Platform: {}{:>9} ({}){}\n'''.format(bcolors.OKBLUE,
                                     "... ",
                                     " ... ",
                                     "... ",
                                     " ... ",
                                     "... ",
	                                 " ... ",
	                                 bcolors.ENDC,
	                                 bcolors.WARNING,
                                     ___author___,
                                     bcolors.ENDC,
                                     bcolors.WARNING,
                                     ___version___,
                                     bcolors.ENDC,
                                     bcolors.WARNING,
                                     platform.system(),
                                     platform.machine(),
                                     bcolors.ENDC), end='\n')
        start_time = time.time()
        self.navigateur = self.Connection(compte)
        self._exception = True

        navigationStart = self.navigateur.execute_script("return window.performance.timing.navigationStart")
        responseStart = self.navigateur.execute_script("return window.performance.timing.responseStart")
        domComplete = self.navigateur.execute_script("return window.performance.timing.domComplete")

        backendPerformance = responseStart - navigationStart
        frontendPerformance = domComplete - responseStart
        self.ut = Utils(self.navigateur)

        start_time_login = time.time()
        login = self.InputLogin(self.navigateur, compte, password)
        interval_login = time.time() - start_time_login
        if login is False:
            login_retry = self.InputLogin(self.navigateur, compte, password, True)
            if login_retry is False:
                try:
                    self.close(self.navigateur)
                except (IndexError, SessionNotCreatedException):
                    self._exception = ValueError("divisor must not be zero")
                finally:
                    if self._exception:
                        print("close normal")
                        try:
                            self.close(self.navigateur)
                        except SessionNotCreatedException:
                            exit(0)

        print("\033[92m" + 'Total time login in seconds:', str(interval_login) + "\033[0m")
        # self.deletepopup(self.navigateur)
        try:
            if sys.argv[3] == "cv":
                self.cv(self.navigateur)

            if sys.argv[3] == "check":
                actualisationcheck = self.actualisation(self.navigateur)
                if actualisationcheck is False:
                    print(bcolors.FAIL + "Vous êtes déja actualisez... ou le bouton n'est pas mis en avant." + bcolors.ENDC)
            if sys.argv[3] == "search":
                search = self.search(self.navigateur)

        except (IndexError, TimeoutException):
            try:
                for i in range(0, 9):
                    if sys.argv[3] == "cv":
                        cv = self.cv(self.navigateur)
                        if cv:
                            break

                    if sys.argv[3] == "check":
                        actualisationcheck = self.actualisation(self.navigateur)
                        if actualisationcheck is False:
                            print("{}Vous êtes déja actualisez... ou le bouton n'est pas mis en avant.{}".format(bcolors.FAIL, bcolors.ENDC))
                            break

                    if sys.argv[3] == "search":
                        while 1:
                            search = self.search(self.navigateur)
            except (TimeoutException, IndexError):
                pass

        print()
        print("\033[95m \033[1mBack End: %s ms \033[0m" % backendPerformance)
        print("\033[95m \033[1mFront End: %s ms \033[0m" % frontendPerformance)

        interval = time.time() - start_time
        print('\033[95m \033[1mTotal time in seconds:', str(interval) + "\033[0m")
        print()

        try:
            if sys.argv[4] != "noclose" and len(sys.argv) == 4 or display is False:
                print("close normal")
                self.close(self.navigateur)
            elif sys.argv[3] != "noclose" and len(sys.argv) == 3 or display is False:
                print("close normal")
                self.close(self.navigateur)
        except (IndexError, SessionNotCreatedException):
            self._exception = ValueError("divisor must not be zero")

    def page_has_loaded(self, navigateur):
        page_state = navigateur.execute_script('return document.readyState')
        if page_state == 'complete':
            detect_jquery = navigateur.execute_script('return window.jQuery != undefined')
            if detect_jquery:
                detect_jquery = navigateur.execute_script('return jQuery.active == 0')
                if detect_jquery:
                    print("Page Load Success !")
                    return True
        return False

    '''
    it's used for define broswer selenium and Profile option
    '''
    def Connection(self, account):
        print(bcolors.OKGREEN + "Connection au Pole Emploi" + bcolors.ENDC)

        url = "https://candidat.pole-emploi.fr/candidat/espacepersonnel/authentification/"
        if os.path.isdir("/home/" + account) is False:
            os.makedirs("/home/" + account)
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0")
        caps = DesiredCapabilities.FIREFOX.copy()
        caps['specificationLevel'] = 1
        navigateur = webdriver.Firefox(capabilities=caps)
        navigateur.set_window_size(1000, 1000)
        navigateur.get(url)
        return navigateur

    '''
    Function to login page enter input ID +
    search and define password
    '''
    def InputLogin(self, navigateur, account, password, resend=False):
        getsize = navigateur.get_window_size()
        print("{}Fix size (Width: {} Height: {}){}".format(bcolors.OKBLUE, getsize['width'], getsize['height'], bcolors.ENDC))
        if resend:
            url = "https://candidat.pole-emploi.fr/candidat/espacepersonnel/authentification/"
            navigateur.get(url)

        # input ID
        page_load = self.page_has_loaded(navigateur)
        if page_load:
            inputs = self.ut.retry(method=By.XPATH, element="//input[@name='callback_0']",
                                   objects="input", send_keys=account, method_input=By.ID,
                                   element_input="submit", message="Enter ID with input",
                                   message_fail="Timeout check element recheck...",
                                   timeout=10, check_login=True, timeout_fail=10, retry=5)
            if inputs is False:
                return False

            # wait for load pad
            for a, i in enumerate(range(0,9)):
                cel_0 = self.ut.retry(method=By.ID,
                                      element="val_cel_"+str(i),
                                      objects="single_element",
                                      timeout=8, retry=3)
                if cel_0:
                    print("\033[F\033[K\033[1A")
                    if i == 0:
                        a = i+1
                    if i == 9:
                        a = i+10
                    percent = 10*(a+1)+10
                    if percent != 100:
                        print("{}{}\n{} {}{}".format(bcolors.WARNING, "Loading pad ...", "#"*(i*2), percent, "%", bcolors.ENDC))
                        print("\033[F\033[1A")
                    else:
                        print("{}{}\n{} {}{}".format(bcolors.OKBLUE, "Loading pad ...","#"*(i*2), percent, "%", bcolors.ENDC))


            if cel_0:
                navigateur.save_screenshot('images/screenshot.png')
                liste = list(password)
            else:
                exit()

            for i in range(0, 10):
                cel_0 = self.ut.retry(method=By.ID,
                                      element="val_cel_"+str(i),
                                      objects="single_element",
                                      timeout=0.01, retry=3)
                location = cel_0.location
                size = cel_0.size
                im = Image.open('images/screenshot.png')
                left = location['x']
                top = location['y']
                right = location['x'] + size['width']
                bottom = location['y'] + size['height']
                im = im.crop((left, top, right, bottom))  # defines crop points
                im.save('images/Downloads/cel_'+str(i)+'.png')  # saves new cropped image

            dict_pass = {}
            if os.path.isdir("images/Downloads") is False:
                os.makedirs("images/Downloads")

            # prepare list for password dual loop [(0,0), (0, 1), ... (0, 9), (1, 0), (1, 1), ...]
            listes = [(x, y) for x in range(0, 10) for y in range(0, 10)]

            print(bcolors.OKBLUE + "Analysing Pad ... please wait" + bcolors.ENDC)
            start_time_login = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                for a, i in listes:
                    lineexec = executor.submit(calcule_image,
                                               'cel_'+str(i)+'.png', a, number_detect_firefox)
                    if lineexec.result() is True:
                        # print("cel_"+str(i), " = "+str(a))
                        elem = self.ut.retry(method=By.XPATH,
                                             element="//button[@id='"+"val_cel_"+str(i)+"']",
                                             objects="single_element", timeout=0.01, retry=3)
                        dict_pass[elem.get_attribute("class")] = list()
                        dict_pass[elem.get_attribute("class")].append(a)
                        dict_pass[elem.get_attribute("class")].append(elem.get_attribute("id"))

            interval_login = time.time() - start_time_login

            callback_string = ""
            listes = [(x, y, z) for x in liste for y, z in dict_pass.items()]
            for attrib, key, value in listes:
                if int(attrib) == value[0]:
                    # button = WebDriverWait(navigateur, 0.01).until(EC.presence_of_element_located((By.XPATH, "//button[@class='"+key+"']")))
                    # print(key, value[0], value[1])
                    callback_string += value[1]
                    # button.click()

            if callback_string == "":
                return False

            navigateur.execute_script("document.getElementById(\"idTouchesCliques\").value=\""+callback_string+"\";")

            elem = self.ut.retry(method=By.XPATH,
                                 element="//input[@id='idTouchesCliques']",
                                 objects="single_element", timeout=0.01,
                                 message="resolved pad touch '"+callback_string+"'",
                                 color=bcolors.OKBLUE, retry=3)

            print(bcolors.UNDERLINE + bcolors.BOLD + bcolors.OKBLUE +
                  'resolve pad time in seconds:', str(interval_login) +
                  bcolors.ENDC)

            # inputPostal = navigateur.find_element_by_id("champTexteCodePostal")
            inputPostal = self.ut.retry(method=By.ID,
                                        element="codepostal", objects="single_element",
                                        timeout=3, retry=3)
            inputPostal.send_keys(data_loaded[sys.argv[2]][2])
            inputPostal.send_keys(Keys.RETURN)
            return True
        else:
            return False

    '''
    Delete popup 'fancybox if show'
    '''
    def deletepopup(self, navigateur):
        try:
            inputspan = self.ut.retry(method=By.XPATH,
                                      element="//*[@class='js-close-popin']",
                                      objects="click_element", timeout=5, retry=3)
            return True
        except (TimeoutException, ElementNotInteractableException):
            return False
    '''
    clean html preparsed
    '''
    def cleanhtml(self, raw_html):
        raw_html = re.sub('<[^<]+?>', '', raw_html)
        raw_html = re.sub(r'\([^)]*\)', '', raw_html)
        cleantext = re.sub('(rafraîchir ce CV)', '', raw_html)
        return cleantext

    '''
    function search offer job it's used for search job and parse text
    While loop use
    '''
    def search_result(self, navigateur, ids, back, page_start, page_stop, row):
        ids = ids-(row*10)
        elem = self.ut.retry(method=By.XPATH,
                             element="//ul[@id='page_"+page_start+"-"+page_stop+"']/li[@class='result']["+str(ids+1)+"]/div[@id='"+str(ids)+"']/div[@class='media-body']/h2/a",
                             objects="click_element", timeout=1, retry=3)

        time.sleep(1)
        for i, elem in enumerate(self.ut.retry(method=By.XPATH,
                                               element="//div[@id='detailOffreVolet']",
                                               objects="all_elements", timeout=8, retry=3)):
            soup = BeautifulSoup(elem.get_attribute("innerHTML"), 'lxml')  # Parse the HTML as a string
            print()
            print("{}{}{}".format(bcolors.WARNYELLOW,
                                  self.ut.cleanhtmls(str(soup.find_all("h2",
                                                                       class_="t2 title")[0])),
                                  bcolors.ENDC))

            print("{}{}{}".format(bcolors.OKGREEN,
                                  self.ut.cleanhtmls(str(soup.find_all("p",
                                                                       class_="t4 title-complementary")[0])),
                                  bcolors.ENDC))

            print("{}{}{}".format(bcolors.OKGREEN,
                                  self.ut.cleanhtmls(str(soup.find_all("p",
                                                                       class_="t5 title-complementary")[0])),
                                  bcolors.ENDC))
            print()
            print("{}{}{}".format(bcolors.OKBLUE,
                                  self.ut.cleanhtmls(str(soup.find_all("div",
                                                                       class_="description col-sm-8 col-md-7")[0])),
                                  bcolors.ENDC))
            print()
            for i in soup.find_all("dd"):
                print("{}{}{}".format(bcolors.OKBLUE,
                                      self.ut.cleanhtmls(str(i)),
                                      bcolors.ENDC))
            print()
            print("{}Profil souhaité{}".format(bcolors.WARNYELLOW, bcolors.ENDC))
            print()
            for a, i in enumerate(soup.find_all("ul",
                                                class_="skill-list list-unstyled")):
                if a == 0:
                    print("{}{}{}".format(bcolors.OKBLUE, "[Expérience]", bcolors.ENDC))
                    print("{}{}{}".format(bcolors.OKGREEN, self.ut.cleanhtmls(str(i)), bcolors.ENDC))
                if a == 1:
                    print("{}{}{}".format(bcolors.OKBLUE, "[Compétences]", bcolors.ENDC))
                    c = i.find_all("span", class_="skill-name")
                    d = i.find_all("span", class_="skill-required")
                    c.append("")
                    d.append("")
                    for x, y in zip(c, d):
                        if x and y:
                            print("{}{}{}{}{}".format(self.ut.cleanhtmls(str(x)),
                                                      " - ", bcolors.WARNING,
                                                      self.ut.cleanhtmls(str(y)),
                                                      bcolors.ENDC))
                        else:
                            print(self.ut.cleanhtmls(str(x)))

                if a == 2:
                    print("{}{}{}".format(bcolors.OKBLUE, "[Formation]", bcolors.ENDC))
                    c = i.find_all("span", class_="skill-name")
                    d = i.find_all("span", class_="skill-required")
                    c.append("")
                    d.append("")
                    for x, y in zip(c, d):
                        if x and y:
                            print("{}{}{}{}{}".format(self.ut.cleanhtmls(str(x)),
                                                      " - ", bcolors.WARNING,
                                                      self.ut.cleanhtmls(str(y)),
                                                      bcolors.ENDC))
                        else:
                            print(self.ut.cleanhtmls(str(x)))
                print()

        while 1:

            select = input(" [m] enregistrer dans le mémo \n [p] pour postuler \n [x] pour quitter \n Séléctionner l'action qui vous intéresse: ")

            """try:
                elem = WebDriverWait(navigateur, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='close glaze-exclude']")))
                elem.click()
            except TimeoutException:
                continue"""

            if select == "m":
                pass

            if select == "p":
                try:
                    self.ut.retry(method=By.XPATH,
                                  element="//div[@id='contactOffreVolet']/p[@class='btn-container']/a",
                                  objects="click_element", timeout=5, retry=3)

                    elem = self.ut.retry(method=By.XPATH,
                                         element="//div[@class='main-content']/div[@class='bd']/p",
                                         objects="single_element", message="return_cleanhtml",
                                         timeout=5, retry=3)
                    count_cv = 0

                    for i, elem in enumerate(self.ut.retry(method=By.XPATH,
                                                           element="//div[@class='main-content']/div[@class='bd']/fieldset/div[@class='block group value']/div[@class='outer-block']/div[@class='hd']/h3",
                                                           objects="all_elements", timeout=8, retry=3)):

                        print("{}{}{}{}{}".format(bcolors.OKGREEN,
                                                  " --- ",
                                                  self.ut.cleanhtmls(elem.get_attribute("innerHTML")),
                                                  " ---", bcolors.ENDC))

                        for elem in self.ut.retry(method=By.XPATH,
                                                  element="//div[@class='main-content']/div[@class='bd']/fieldset/div[@class='block group value']/div[@class='outer-block']/div[@class='bd']["+str(i+1)+"]/fieldset/div[@class='parallel-block-3-2']",
                                                  objects="all_elements", timeout=8, retry=3):

                            print("{}{}{}{}{}".format(str(count_cv),
                                                      " -", bcolors.OKBLUE,
                                                      self.ut.cleanhtmls(elem.get_attribute("innerHTML")),
                                                      bcolors.ENDC))
                            count_cv = count_cv + 1
                        print()

                    cv_choisi = input("Séléctionner le cv [0-"+str(count_cv-1)+"]:")

                    for i, elem in enumerate(self.ut.retry(method=By.XPATH,
                                                           element="//input[@type='radio']",
                                                           objects="all_elements", timeout=8, retry=3)):
                        if i == int(cv_choisi):
                            elem.click()

                    self.ut.retry(method=By.XPATH,
                                  element="//input[@value='Valider']",
                                  objects="click_element", timeout=5, retry=3)

                    time.sleep(1)
                    self.ut.retry(method=By.XPATH,
                                  element="//button[@title='Envoyer']",
                                  objects="click_element", timeout=5, retry=3)

                    print("Vous avez postulez correctement à l'annonce.")
                    break
                    return False
                except TimeoutException:
                    continue

            if select == "x" or select == "X":
                navigateur.get(back)
                return True

        return False

    '''
    initialise search job find try to find element in page
    and use while loop
    '''
    def search(self, navigateur):
        time.sleep(3)
        self.navigateur.get("https://candidat.pole-emploi.fr/offres/recherche?offresPartenaires=true&rayon=10&tri=0")

        navigateur.execute_script("document.getElementById(\"idoffresPartenaires\").checked = false;")
        search_input = input("Séléctionner votre recherche: ")
        inputs = self.ut.retry(method=By.XPATH,
                               element="//input[@id='idmotsCles-selectized']",
                               objects="single_element", timeout=5, retry=3)
        inputs.click()
        inputs.send_keys(search_input)
        time.sleep(0.05)

        valide = self.ut.retry(method=By.XPATH,
                               element="//ul[@class='selectize-dropdown-content']/li[1]",
                               objects="click_element", timeout=10, retry=3)

        position_input = input("Séléctionner votre lieux de recherche: ")
        inputs = self.ut.retry(method=By.XPATH,
                               element="//input[@id='idlieux-selectized']",
                               objects="single_element", timeout=5, retry=3)
        inputs.click()

        for i in range(0, len(position_input)):
            time.sleep(0.01)
            inputs.send_keys(position_input[i])

        inputs = self.ut.retry(method=By.XPATH,
                               element="//ul[@class='selectize-dropdown-content']/li[1]",
                               element_retry="//ul[@class='selectize-dropdown-content']/li[1]",
                               objects="force_find_click", timeout=5, retry=3)

        button = self.ut.retry(method=By.XPATH,
                               element="//a[@id='btnSubmitRechercheForm']",
                               objects="click_element", message="return_cleanhtml",
                               color=bcolors.OKBLUE, timeout=10, retry=3)

        print(""" RESULT SEARCH """)
        for i, elem in enumerate(self.ut.retry(method=By.XPATH,
                                     element="//div[@class='media-body']",
                                     objects="all_elements", timeout=8, retry=3)):
            soup = BeautifulSoup(elem.get_attribute("innerHTML"), 'lxml')  # Parse the HTML as a string
            print("{}{}{}{}{}".format(str(i),
                                      " ", bcolors.WARNYELLOW,
                                      self.ut.cleanhtmls(str(soup.find_all("h2")[0])).strip(),
                                      bcolors.ENDC))
            for a in range(0, len(soup.find_all("p"))):
                if a == 0:
                    print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[0])),
                                                  bcolors.ENDC,
                                                  "\n", bcolors.OKBLUE,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[1])),
                                                  bcolors.ENDC))
                if a == 1:
                    print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[2])),
                                                  bcolors.ENDC,
                                                  "\n", bcolors.OKBLUE,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[3])),
                                                  bcolors.ENDC))

            print()
            # print(self.ut.cleanhtmls(str(soup.find_all("h2")[0])).strip() + bcolors.ENDC)

        row = 0
        urls = []
        while 1:
            if row == 0:
                start = 0
                end = 9
                start_row = 10
                end_row = 19

            select = input(" ["+str(start)+"-"+str(end)+"] ou pour plus de recherche [+] \n [s] pour revoir la liste des offres \n [x] pour quitter \n Séléctionner l'offre qui vous intéresse: ")
            try:
                if re.search('\d+', select):
                    if int(select) >= start and int(select) <= end:
                        urls.append(navigateur.current_url)
                        try:
                            button = self.ut.retry(method=By.XPATH,
                                                   element="//button[@class='eupopup-closebutton btn-reset']",
                                                   objects="click_element",
                                                   message="close automatical 'fancy box'",
                                                   color=bcolors.OKBLUE, timeout=1, retry=1)
                        except (TimeoutException, ElementNotInteractableException, AttributeError):
                            pass
                        try:
                            result = self.search_result(navigateur, int(select), urls[0], str(start), str(end), row)
                            if result is False:
                                break
                        except (TimeoutException, ElementNotInteractableException):
                            for i in range(0, 3):
                                print("trying... resolve search")
                                try:
                                    result = self.search_result(navigateur, int(select), urls[0], str(start), str(end), row)
                                    if result is False:
                                        break
                                except (TimeoutException, ElementNotInteractableException):
                                    navigateur.get(navigateur.current_url)
                                    time.sleep(0.5)

                                    for i in range(0, row):
                                        time.sleep(0.3)
                                        plus = self.ut.retry(method=By.XPATH,
                                                             element="//p[@id='zoneAfficherPlus']/a",
                                                             objects="click_element", timeout=10, retry=1)

                                    result = self.search_result(navigateur, int(select), urls[0], str(start), str(end), row)
                                    if result is False:
                                        break
            except ValueError:
                pass

            if isinstance(select, str) and select == "x" or select == "X":
                break

            if isinstance(select, str) and select == "s" or select == "S":
                try:
                    for i, elem in enumerate(self.ut.retry(method=By.XPATH,
                                                           element="//ul[@id='page_"+str(start)+"-"+str(end)+"']/li[@class='result']/div/div[@class='media-body']",
                                                           objects="all_elements", timeout=1, retry=3)):
                        soup = BeautifulSoup(elem.get_attribute("innerHTML"), 'lxml')  # Parse the HTML as a string
                        print("{}{}{}{}{}".format(str(start+i),
                                        " ", bcolors.WARNYELLOW,
                                        self.ut.cleanhtmls(str(soup.find_all("h2")[0])).strip(),
                                        bcolors.ENDC))
                        for a in range(0, len(soup.find_all("p"))):
                            if a == 0:
                                print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                                     self.ut.cleanhtmls(str(soup.find_all("p")[0])),
                                                     bcolors.ENDC, "\n", bcolors.OKBLUE,
                                                     self.ut.cleanhtmls(str(soup.find_all("p")[1])),
                                                     bcolors.ENDC))
                            if a == 1:
                                print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                                      self.ut.cleanhtmls(str(soup.find_all("p")[2])),
                                                      bcolors.ENDC,
                                                      "\n", bcolors.OKBLUE,
                                                      self.ut.cleanhtmls(str(soup.find_all("p")[3])),
                                                      bcolors.ENDC))
                        print()
                except (TimeoutException, ElementNotInteractableException):
                    for i in range(0, 3):
                        # print("trying... resolve search")
                        try:
                            for i, elem in enumerate(self.ut.retry(method=By.XPATH,
                                                                   element="//ul[@id='page_"+str(start)+"-"+str(end)+"']/li[@class='result']/div/div[@class='media-body']",
                                                                   objects="all_elements", timeout=1, retry=3)):

                                soup = BeautifulSoup(elem.get_attribute("innerHTML"), 'lxml')  # Parse the HTML as a string
                                print("{}{}{}{}{}".format(str(start+i),
                                              " ", bcolors.WARNYELLOW,
                                              self.ut.cleanhtmls(str(soup.find_all("h2")[0])).strip(),
                                              bcolors.ENDC))

                                for a in range(0, len(soup.find_all("p"))):
                                    if a == 0:
                                        print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[0])),
                                                  bcolors.ENDC, "\n",
                                                  bcolors.OKBLUE,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[1])),
                                                  bcolors.ENDC))
                                    if a == 1:
                                        print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[2])),
                                                  bcolors.ENDC,
                                                  "\n", bcolors.OKBLUE,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[3])),
                                                  bcolors.ENDC))
                                print()
                        except (TimeoutException, ElementNotInteractableException):
                            navigateur.get(navigateur.current_url)
                            time.sleep(0.5)

                            for i in range(0, row):
                                time.sleep(0.3)
                                plus = self.ut.retry(method=By.XPATH,
                                                     element="//p[@id='zoneAfficherPlus']/a",
                                                     objects="click_element", timeout=10, retry=3)

                            for i, elem in enumerate(self.ut.retry(method=By.XPATH,
                                    element="//ul[@id='page_"+str(start)+"-"+str(end)+"']/li[@class='result']/div/div[@class='media-body']",
                                    objects="all_elements", timeout=1, retry=3)):

                                soup = BeautifulSoup(elem.get_attribute("innerHTML"), 'lxml')  # Parse the HTML as a string
                                print("{}{}{}{}{}".format(str(start+i),
                                                " ", bcolors.WARNYELLOW,
                                                self.ut.cleanhtmls(str(soup.find_all("h2")[0])).strip(),
                                                bcolors.ENDC))
                                for a in range(0, len(soup.find_all("p"))):
                                    if a == 0:
                                        print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[0])),
                                                  bcolors.ENDC, "\n",
                                                  bcolors.OKBLUE,
                                                  self.ut.cleanhtmls(str(soup.find_all("p")[1])),
                                                  bcolors.ENDC))
                                    if a == 1:
                                        print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                                 self.ut.cleanhtmls(str(soup.find_all("p")[2])),
                                                 bcolors.ENDC, "\n",
                                                 bcolors.OKBLUE,
                                                 self.ut.cleanhtmls(str(soup.find_all("p")[3])),
                                                 bcolors.ENDC))
                                print()
                        if soup:
                            break

            if isinstance(select, str) and select == "+":
                if row == 0:
                    fancy = self.ut.retry(method=By.XPATH,
                                element="//button[@class='eupopup-closebutton btn-reset']",
                                objects="click_element", timeout=10, retry=3)
                    if fancy:
                        print(bcolors.OKBLUE+"close automatical 'fancy box'"+bcolors.ENDC)
                self.navigateur.execute_script('const elements = document.getElementsByClassName("loader-container"); while (elements.length > 0) elements[0].remove();')

                plus = self.ut.retry(method=By.XPATH,
                              element="//p[@id='zoneAfficherPlus']/a",
                              objects="click_element", timeout=10, retry=3)
                time.sleep(1)
                plus = self.ut.retry(method=By.XPATH,
                                     element="//p[@id='zoneAfficherPlus']/a",
                                     objects="single_element", timeout=10, retry=3, actions="perform")

                self.navigateur.execute_script("return arguments[0].scrollIntoView();", plus)

                print(""" RESULT SEARCH """)
                start = end+1
                end = start+9
                start_row = end_row+1
                end_row = start_row+9

                time.sleep(0.1)
                for i, elem in enumerate(self.ut.retry(method=By.XPATH,
                                                       element="//ul[@id='page_"+str(start)+"-"+str(end)+"']/li[@class='result']/div/div[@class='media-body']",
                                                       objects="all_elements", timeout=8, retry=3)):
                    soup = BeautifulSoup(elem.get_attribute("innerHTML"), 'lxml')  # Parse the HTML as a string

                    print("{}{}{}{}{}".format(str(start+i),
                             " ", bcolors.WARNYELLOW,
                             self.ut.cleanhtmls(str(soup.find_all("h2")[0])).strip(),
                             bcolors.ENDC))

                    for a in range(0, len(soup.find_all("p"))):
                        if a == 0:
                            print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                    self.ut.cleanhtmls(str(soup.find_all("p")[0])),
                                    bcolors.ENDC, "\n", bcolors.OKBLUE,
                                    self.ut.cleanhtmls(str(soup.find_all("p")[1])),
                                    bcolors.ENDC))
                        if a == 1:
                            print("{}{}{}{}{}{}{}".format(bcolors.OKGREEN,
                                     self.ut.cleanhtmls(str(soup.find_all("p")[2])),
                                     bcolors.ENDC, "\n", bcolors.OKBLUE,
                                     self.ut.cleanhtmls(str(soup.find_all("p")[3])),
                                     bcolors.ENDC))
                    print()

                row = row + 1
                print()

        return True

    '''
    shema to find cv page and parse text
    '''
    def cv(self, navigateur):
        print()

        for elem in self.ut.retry(method=By.XPATH,
                                  element="//h2[@class='category-title']/a",
                                  objects="all_elements", timeout=8, retry=3):
            if elem.get_attribute("innerHTML") == "Mes candidatures,<br> CV et propositions":
                print("{}{}{}{}{}".format(bcolors.OKGREEN,
                         "click on '",
                         elem.get_attribute("innerHTML"),
                         "'", bcolors.ENDC))
                elem.click()
                break

        for elem in self.ut.retry(method=By.XPATH,
                                  element="//h2[@class='category-title']/a",
                                  objects="all_elements", timeout=8, retry=3):
            if elem.get_attribute("innerHTML") == "Mes <br>CV":
                print("{}{}{}{}{}".format(bcolors.OKGREEN,
                        "click on '",
                        elem.get_attribute("innerHTML"),
                        "'", bcolors.ENDC))
                elem.click()
                break

        for i, elem in enumerate(self.ut.retry(method=By.XPATH,
                                               element="//h2[@class='block-title']/a",
                                               objects="all_elements", timeout=8, retry=3)):
            print()
            cvspan = self.ut.retry(method=By.XPATH, element="//h2[@class='block-title']/span[@class='date-refresh ng-scope']",
                                   objects="all_elements", timeout=8, retry=3)
            if cvspan:
                print("{}{}{}{}{}{}".format(bcolors.OKBLUE, elem.get_attribute("innerHTML"), " ( ",
                        self.cleanhtml(cvspan[i].get_attribute("outerHTML")).strip(),
                        "(s) ) ", bcolors.ENDC))

            cvsupdate = self.ut.retry(method=By.XPATH,
                                      element="//div[@class='hd']/span[@class='flag-unit']/span[@class='flag-txt ng-binding']",
                                      objects="all_elements", timeout=8, retry=3)
            if cvsupdate:
                print("\033[0;33m"+bcolors.UNDERLINE+bcolors.BOLD+" > "+cvsupdate[i].get_attribute("innerHTML")+" < \033[0m")

            cvspan = self.ut.retry(method=By.XPATH,
                                   element="//div[@class='primary']/div[@class='parallel-unit']/span[@class='value ng-binding']",
                                   objects="all_elements", timeout=8, retry=3)
            print(" > " + cvspan[i].get_attribute("innerHTML"))

    '''
    define for actualisation account in pole emploi
    '''
    def actualisation(self, navigateur):
        try:
            try:
                check_actualisation = self.ut.retry(method=By.XPATH,
                                                    element="//div[@class='feature-unit row-2 u-feature span-3']/div[2]/div[2]/p",
                                                    objects="single_element", timeout=8, retry=3)
                if "Vous avez déjà déclaré votre situation pour cette période" in check_actualisation.get_attribute("innerHTML"):
                    print(bcolors.FAIL + "Vous êtes déjà actualiser." + bcolors.ENDC)
                    return False
            except:
                return False

            for elem in self.ut.retry(method=By.XPATH, element="//span/a",
                                      objects="all_elements",
                                      timeout=8, retry=3):
                if elem.get_attribute("innerHTML") == "Je m'actualise ?":
                    print("click on '" + elem.get_attribute("innerHTML")+"' ")
                    elem.click()
                    break

            # Etes-vous inscrit à une session de formation ou suivez-vous une formation ?
            formationOui = self.ut.retry(method=By.XPATH, element="//label[@for='formationOui']/strong",
                                         objects="single_element", timeout=8, retry=3)
            formationNon = self.ut.retry(method=By.XPATH, element="//label[@for='formationNon']/strong",
                                         objects="single_element", timeout=8, retry=3)

            if data_loaded[sys.argv[2]][3] == "Oui" or data_loaded[sys.argv[2]][3] == "oui":
                print("Etes-vous inscrit à une session de formation ou suivez-vous une formation ? click on 'Oui'")
                formationOui.click()

            if data_loaded[sys.argv[2]][3] == "Non" or data_loaded[sys.argv[2]][3] == "non":
                print("Etes-vous inscrit à une session de formation ou suivez-vous une formation ? click on 'Non'")
                formationNon.click()

            for elem in self.ut.retry(method=By.XPATH, element="//button[@class='js-only']",
                                      objects="all_elements", timeout=8, retry=3):
                if elem.get_attribute("innerHTML") == "Valider":
                    elem.click()
                    break

            # Avez-vous travaillé ?
            TravailleOui = self.ut.retry(method=By.XPATH, element="//label[@for='blocTravail-open']/input",
                                         objects="single_element", timeout=10, retry=3)
            TravailleNon = self.ut.retry(method=By.XPATH, element="//label[@for='blocTravail-close']/input",
                                         objects="single_element", timeout=10, retry=3)

            if data_loaded[sys.argv[2]][4] == "Oui" or data_loaded[sys.argv[2]][4] == "oui":
                print("Avez-vous travaillé ? click on 'Oui'")
                TravailleOui.click()

            if data_loaded[sys.argv[2]][4] == "Non" or data_loaded[sys.argv[2]][4] == "non":
                print("Avez-vous travaillé ? click on 'Non'")
                TravailleNon.click()

            # Avez-vous été en stage ?
            StageOui = self.ut.retry(method=By.XPATH, element="//label[@for='blocStage-open']/input",
                                     objects="single_element", timeout=10, retry=3)
            StageNon = self.ut.retry(method=By.XPATH, element="//label[@for='blocStage-close']/input",
                                     objects="single_element", timeout=10, retry=3)

            if data_loaded[sys.argv[2]][5] == "Oui" or data_loaded[sys.argv[2]][5] == "oui":
                print("Avez-vous été en stage ? click on 'Oui'")
                StageOui.click()

            if data_loaded[sys.argv[2]][5] == "Non" or data_loaded[sys.argv[2]][5] == "non":
                print("Avez-vous été en stage ? click on 'Non'")
                StageNon.click()

            # Avez-vous été en arrêt maladie ?
            MaladieOui = self.ut.retry(method=By.XPATH, element="//label[@for='blocMaladie-open']/input",
                                       objects="single_element", timeout=10, retry=3)
            MaladieNon = self.ut.retry(method=By.XPATH, element="//label[@for='blocMaladie-close']/input",
                                       objects="single_element", timeout=10, retry=3)

            if data_loaded[sys.argv[2]][6] == "Oui" or data_loaded[sys.argv[2]][6] == "oui":
                print("Avez-vous été en arrêt maladie ? click on 'Oui'")
                MaladieOui.click()

            if data_loaded[sys.argv[2]][6] == "Non" or data_loaded[sys.argv[2]][6] == "non":
                print("Avez-vous été en arrêt maladie ? click on 'Non'")
                MaladieNon.click()

            # Percevez-vous une nouvelle pension retraite ?
            RetraiteOui = self.ut.retry(method=By.XPATH, element="//label[@for='blocRetraite-open']/input",
                                        objects="single_element", timeout=10, retry=3)
            RetraiteNon = self.ut.retry(method=By.XPATH, element="//label[@for='blocRetraite-close']/input",
                                        objects="single_element", timeout=10, retry=3)

            if data_loaded[sys.argv[2]][7] == "Oui" or data_loaded[sys.argv[2]][7] == "oui":
                print("Percevez-vous une nouvelle pension retraite ? click on 'Oui'")
                RetraiteOui.click()

            if data_loaded[sys.argv[2]][7] == "Non" or data_loaded[sys.argv[2]][7] == "non":
                print("Percevez-vous une nouvelle pension retraite ? click on 'Non'")
                RetraiteNon.click()

            # Percevez-vous une nouvelle pension d'invalidité de 2ème ou 3ème catégorie ?
            InvaliditeOui = self.ut.retry(method=By.XPATH, element="//label[@for='blocInvalidite-open']/input",
                                          objects="single_element", timeout=10, retry=3)
            InvaliditeNon = self.ut.retry(method=By.XPATH, element="//label[@for='blocInvalidite-close']/input",
                                          objects="single_element", timeout=10, retry=3)

            if data_loaded[sys.argv[2]][8] == "Oui" or data_loaded[sys.argv[2]][8] == "oui":
                print("Percevez-vous une nouvelle pension d'invalidité de 2ème ou 3ème catégorie ? click on 'Oui'")
                InvaliditeOui.click()

            if data_loaded[sys.argv[2]][8] == "Non" or data_loaded[sys.argv[2]][8] == "non":
                print("Percevez-vous une nouvelle pension d'invalidité de 2ème ou 3ème catégorie ? click on 'Non'")
                InvaliditeNon.click()

            # Etes-vous toujours à la recherche d'un emploi ?
            RechercheOui = self.ut.retry(method=By.XPATH, element="//label[@for='blocRecherche-close']/input",
                                         objects="single_element", timeout=10, retry=3)
            RechercheNon = self.ut.retry(method=By.XPATH, element="//label[@for='blocRecherche-open']/input",
                                         objects="single_element", timeout=10, retry=3)

            if data_loaded[sys.argv[2]][9] == "Oui" or data_loaded[sys.argv[2]][9] == "oui":
                print("Etes-vous toujours à la recherche d'un emploi ? click on 'Oui'")
                RechercheOui.click()

            if data_loaded[sys.argv[2]][9] == "Non" or data_loaded[sys.argv[2]][9] == "non":
                print("Etes-vous toujours à la recherche d'un emploi ? click on 'Non'")
                RechercheNon.click()
        except:
            return False

    '''
    Close broswer and exit code
    '''
    def close(self, navigateur):
        navigateur.quit()
        exit(0)
