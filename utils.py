# Dependency for wait element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException
import time
import re

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

class Utils():

    def __init__(self):
        pass

    def cleanhtmls(self, raw_html):
        raw_html = raw_html.replace('<br>', ' ')
        raw_html = re.sub('<[^<]+?>', '', raw_html)
        raw_html = re.sub('&nbsp;', ' ', raw_html)
        raw_html = re.sub('&amp;', '&', raw_html)
        raw_html = raw_html.replace('\t', ' ')
        raw_html = raw_html.replace('\n', ' ')
        return raw_html

    def retry(self, navigateur, **kwargs):
        try:
            kwargs["timeout"]
            kwargs["timeout_fail"]
            kwargs["retry"]
        except KeyError as e:
            if "'timeout'" == str(e):
                kwargs["timeout"] = 10

            if "'timeout_fail'" == str(e):
                kwargs["timeout_fail"] = 10

            if str(e) == "'retry'":
                kwargs["retry"] = 3

        if kwargs["objects"] == "single_element":
            try:
                elements = WebDriverWait(navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                return elements
            except TimeoutException:
                for i in range(0, kwargs["retry"]):
                    try:
                        elements = WebDriverWait(navigateur, kwargs["timeout_fail"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                        return elements
                        break
                    except TimeoutException:
                        pass

        if kwargs["objects"] == "force_find_click":
            try:
                valide = WebDriverWait(navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                valide.click()
            except (TimeoutException, ElementNotInteractableException):
                try:
                    for i in range(0, 500):
                        time.sleep(0.1)
                        valide = WebDriverWait(navigateur, 5).until(EC.presence_of_element_located((kwargs["method"], kwargs["element_retry"])))
                        if valide:
                            print(bcolors.OKBLUE + "séléction automatique '" + self.cleanhtmls(valide.get_attribute("innerHTML")) +"'" + bcolors.ENDC)
                            valide.click()
                            break
                except (TimeoutException, ElementNotInteractableException):
                    pass

        if kwargs["objects"] == "input":
            try:
                inputs = WebDriverWait(navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                print(bcolors.OKBLUE + kwargs["message"] + bcolors.ENDC)
                inputs.send_keys(kwargs["send_keys"])
                #button = navigateur.find_element_by_id("boutonContinuer")
                button = WebDriverWait(navigateur, 2).until(EC.presence_of_element_located((kwargs["method_input"], kwargs["element_input"])))
                button.click()
                return True
            except TimeoutException:
                for i in range(0, kwargs["retry"]):
                    try:
                        print("try for element... (" + str(i)+")")
                        print(bcolors.FAIL + kwargs["message_fail"] + bcolors.ENDC)
                        inputs = WebDriverWait(navigateur, kwargs["timeout_fail"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                        print(bcolors.OKBLUE + kwargs["message"] + bcolors.ENDC)
                        inputs.click()
                        inputs.send_keys(kwargs["send_keys"])
                        #button = navigateur.find_element_by_id("boutonContinuer")
                        button = WebDriverWait(navigateur, kwargs["timeout_fail"]).until(EC.presence_of_element_located((kwargs["method_input"], kwargs["element_input"])))
                        if button and inputs:
                            button.click()
                            return True
                            break
                    except TimeoutException:
                        return False

