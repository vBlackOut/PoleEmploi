# Dependency for wait element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
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

    def __init__(self, navigateur):
        self.navigateur = navigateur

    def cleanhtmls(self, raw_html):
        raw_html = raw_html.replace('<br>', ' ')
        raw_html = re.sub('<[^<]+?>', '', raw_html)
        raw_html = re.sub('&nbsp;', ' ', raw_html)
        raw_html = re.sub('&amp;', '&', raw_html)
        raw_html = raw_html.replace('\t', ' ')
        raw_html = raw_html.replace('\n', ' ')
        return raw_html


    def hover(self, element):
        hov = ActionChains(self.navigateur).move_to_element(element)
        hov.perform()

    def retry(self, **kwargs):

        try:
            kwargs["timeout"]
        except KeyError as e:
            if "'timeout'" == str(e):
                kwargs["timeout"] = 10

        try:
            kwargs["timeout_fail"]
        except KeyError as e:
            if "'timeout_fail'" == str(e):
                kwargs["timeout_fail"] = 10

        try:
            kwargs["retry"]
        except KeyError as e:
            if str(e) == "'retry'":
                kwargs["retry"] = 3

        try:
            kwargs["message"]
        except KeyError as e:
            if str(e) == "'message'":
                kwargs["message"] = ""

        try:
            kwargs["actions"]
        except KeyError as e:
            if str(e) == "'actions'":
                kwargs["actions"] = ""

        try:
            kwargs["color"]
        except KeyError as e:
            if str(e) == "'color'":
                kwargs["color"] = bcolors.OKBLUE

        if kwargs["objects"] == "single_element":
            try:
                elements = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))

                if kwargs["message"] == "return_cleanhtml":
                    print(kwargs["color"] + self.cleanhtmls(elements.get_attribute("innerHTML")) + bcolors.ENDC)
                elif kwargs["message"] == "return":
                    print(kwargs["color"] + elements.get_attribute("innerHTML") + bcolors.ENDC)
                else:
                    if kwargs["message"] != "":
                        print(kwargs["color"] + kwargs["message"] + bcolors.ENDC)
                if kwargs["actions"] == "perform":
                    self.hover(elements)

                return elements
            except TimeoutException:
                for i in range(0, kwargs["retry"]):
                    try:
                        elements = WebDriverWait(self.navigateur, kwargs["timeout_fail"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                        if kwargs["actions"] == "perform":
                            self.hover(elements)
                        return elements
                        break
                    except TimeoutException:
                        continue

        if kwargs["objects"] == "click_element":
            try:
                valide = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                if kwargs["message"] == "return_cleanhtml":
                    print(kwargs["color"] + "click on '" + self.cleanhtmls(valide.get_attribute("innerHTML"))+ "'" + bcolors.ENDC)
                elif kwargs["message"] == "return":
                    print(kwargs["color"] + "click on '" + valide.get_attribute("innerHTML")+ "'" + bcolors.ENDC)
                else:
                    if kwargs["message"] != "":
                        print(kwargs["color"] + kwargs["message"] + bcolors.ENDC)

                valide.click()
                return True
            except (TimeoutException, ElementNotInteractableException):
                for i in range(0, 500):
                    try:
                        time.sleep(0.1)
                        valide = WebDriverWait(self.navigateur, kwargs["timeout_fail"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))

                    except (TimeoutException, ElementNotInteractableException):
                        return False

                    if valide:
                        self.hover(valide)
                        valide.click()
                        return True


        if kwargs["objects"] == "force_find_click":
            try:
                valide = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                self.hover(valide)
                valide.click()
                return True
            except (TimeoutException, ElementNotInteractableException):
                try:
                    for i in range(0, 500):
                        time.sleep(0.1)
                        valide = WebDriverWait(self.navigateur, kwargs["timeout_fail"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element_retry"])))
                        if valide:
                            print(bcolors.OKBLUE + "séléction automatique '" + self.cleanhtmls(valide.get_attribute("innerHTML")) +"'" + bcolors.ENDC)
                            self.hover(valide)
                            valide.click()
                            return True
                except (TimeoutException, ElementNotInteractableException):
                    pass

        if kwargs["objects"] == "input":
            print(bcolors.OKBLUE + kwargs["message"] + bcolors.ENDC)
            try:
                inputs = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                inputs.send_keys(kwargs["send_keys"])
                #button = self.navigateur.find_element_by_id("boutonContinuer")
                button = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((kwargs["method_input"], kwargs["element_input"])))
                self.hover(button)
                button.click()
                return True
            except (TimeoutException, ElementNotInteractableException):
                for i in range(0, kwargs["retry"]):
                    print("try for element... (" + str(i)+")")
                    print(bcolors.FAIL + kwargs["message_fail"] + bcolors.ENDC)
                    try:
                        inputs = WebDriverWait(self.navigateur, kwargs["timeout_fail"]).until(EC.presence_of_element_located((kwargs["method"], kwargs["element"])))
                        inputs.send_keys(kwargs["send_keys"])
                        #button = self.navigateur.find_element_by_id("boutonContinuer")
                        button = WebDriverWait(self.navigateur, kwargs["timeout_fail"]).until(EC.presence_of_element_located((kwargs["method_input"], kwargs["element_input"])))
                        self.hover(button)
                        button.click()
                        print(bcolors.OKBLUE + kwargs["message"] + bcolors.ENDC)
                        return True
                    except TimeoutException:
                        continue
            if kwargs["check_login"]:
                    check_login = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((kwargs["method"], "//span[@id='erreur_identifiant']")))
                    if check_login.get_attribute("innerHTML"):
                        return False
            return False


        if kwargs["objects"] == "all_elements":
            try:
                elem = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_all_elements_located((kwargs["method"], kwargs["element"])))
                if kwargs["message"] == "return_cleanhtml":
                    print(kwargs["color"] + "'" + self.cleanhtmls(elem.get_attribute("innerHTML"))+ "'" + bcolors.ENDC)
                elif kwargs["message"] == "return":
                    print(kwargs["color"] + "'" + elem.get_attribute("innerHTML")+ "'" + bcolors.ENDC)
                else:
                    if kwargs["message"] != "":
                        print(kwargs["color"] + kwargs["message"] + bcolors.ENDC)
                return elem
            except TimeoutException:
                for i in range(0, kwargs["retry"]):
                    try:
                        elem = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_all_elements_located((kwargs["method"], kwargs["element"])))
                        if elem:
                            if kwargs["message"] == "return_cleanhtml":
                                print(kwargs["color"] + "'" +self.cleanhtmls(elem.get_attribute("innerHTML"))+ "'" + bcolors.ENDC)
                            elif kwargs["message"] == "return":
                                print(kwargs["color"] + "'" + elem.get_attribute("innerHTML") + "'" + bcolors.ENDC)
                            else:
                                if kwargs["message"] != "":
                                    print(kwargs["color"] + kwargs["message"] + bcolors.ENDC)
                            return elem
                    except TimeoutException:
                        continue
