# dependency for Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

# Dependency for wait element
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Dependancy for other element
import urllib
import time
import pickle
import string
import os
from PIL import Image
from config_bot import *
import sys
import re
import concurrent.futures

# Cookie saver
def save_cookies(driver, file_path):
    LINE = "{domain} False {path} {secure} {expiry} {name} {value}\n"
    with open(file_path, 'w') as file:
        for cookie in driver.get_cookies():
            file.write(
                LINE.format(
                    **cookie))


def load_cookies(driver, file_path):
    with open(file_path, 'r') as file:
        driver.execute_script(
            file.read())

def image_diff(i1, i2):
    i1 = Image.open(i1)
    i2 = Image.open(i2)
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."
 
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
       # for gray-scale jpegs
       dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
       dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
 
    ncomponents = i1.size[0] * i1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents

def check_images(image1, image2):
    pourcent = image_diff(image1, image2)
    #print(pourcent)
    if pourcent <= 0.19:
    	return True
    else:
    	return False

class PoleEmplois():

    def __init__(self, compte, password, display):
        start_time = time.time()
        self.display = self.Afficheur(display) 
        self.navigateur = self.Connection(compte)

        navigationStart = self.navigateur.execute_script("return window.performance.timing.navigationStart")
        responseStart = self.navigateur.execute_script("return window.performance.timing.responseStart")
        domComplete = self.navigateur.execute_script("return window.performance.timing.domComplete")

        backendPerformance = responseStart - navigationStart
        frontendPerformance = domComplete - responseStart

        start_time_login = time.time()
        self.InputLogin(self.navigateur, compte, password)
        interval_login = time.time() - start_time_login
        print('Total time login in seconds:',interval_login)


        
        if sys.argv[3] == "cv":
            self.cv(self.navigateur)

        if sys.argv[3] == "check":
            self.actualisation(self.navigateur)

        print()
        print("Back End: %s ms" % backendPerformance)
        print("Front End: %s ms" % frontendPerformance)

        interval = time.time() - start_time
        print('Total time in seconds:',interval)
        print()

        try:
            if sys.argv[4] != "noclose":
                print("close normal")
                self.close(self.navigateur)
            elif sys.argv[3] != "noclose" and len(sys.argv) == 3:
                print("close normal")
                self.close(self.navigateur)
        except IndexError:
            print("close normal")
            self.close(self.navigateur)


    def Afficheur(self, display):
        if display == True:
            afficheur = Display(visible=1, size=(1024, 800))
            afficheur.start()
        else:
            afficheur = Display(visible=0, size=(1024, 800))
            afficheur.start()


    def Connection(self, account):

        url = "https://candidat.pole-emploi.fr/candidat/espacepersonnel/authentification/"
        profile = webdriver.FirefoxProfile()
        if os.path.isdir("/home/" + account) == False:
            os.makedirs("/home/" + account)
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference("javascript.enabled", 0)
        profile.set_preference('browser.download.dir', "/home/" + account + "/")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        profile.set_preference("pdfjs.disabled", True)
        navigateur = webdriver.Firefox(profile)
        navigateur.get(url)

        return navigateur

    def InputLogin(self, navigateur, account, password):
        # input ID
        inputEmail = WebDriverWait(navigateur, 9).until(EC.presence_of_element_located((By.ID, "identifiant")))
        inputEmail.send_keys(account)
        #button = navigateur.find_element_by_id("boutonContinuer")
        button = WebDriverWait(navigateur, 9).until(EC.presence_of_element_located((By.ID, "submit")))
        button.click()

        liste = list(password)
        start_time_login = time.time() 
        time.sleep(0.11)
        navigateur.save_screenshot('images/screenshot.png')
        for i in range(0,10):
            cel_0 = WebDriverWait(navigateur, 10).until(EC.presence_of_element_located((By.ID, "val_cel_"+str(i))))
            location = cel_0.location
            size = cel_0.size
            im = Image.open('images/screenshot.png')
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            im = im.crop((left, top, right, bottom)) # defines crop points
            im.save('images/Downloads/cel_'+str(i)+'.png') # saves new cropped image

        dict_pass = {}
        if os.path.isdir("images/Downloads") == False:
            os.makedirs("images/Downloads")
        
        # prepare list for password dual loop [(0,0), (0, 1), ... (0, 9), (1, 0), (1, 1), ...]
        listes = [(x, y) for x in range(0, 10) for y in range(0, 10)]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for a, i in listes:
                lineexec = executor.submit(check_images, 'images/Downloads/cel_'+ str(i) +'.png', 'images/Templates/normal/'+str(a)+'.png')
                if lineexec.result() == True:
                    #print("cel_"+str(i), " = "+str(a))
                    elem = WebDriverWait(navigateur, 9.5).until(EC.presence_of_element_located((By.XPATH, "//button[@id='"+"val_cel_"+str(i)+"']")))
                    dict_pass[elem.get_attribute("class")] = a

        if sum(map(len, dict_pass.values())) < 9:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                for a, i in listes:
                    lineexec = executor.submit(check_images, 'images/Downloads/cel_'+ str(i) +'.png', 'images/Templates/1600x900/'+str(a)+'.png')
                    if lineexec.result() == True:
                        #print("cel_"+str(i), " = "+str(a))
                        elem = WebDriverWait(navigateur, 9.5).until(EC.presence_of_element_located((By.XPATH, "//button[@id='"+"val_cel_"+str(i)+"']")))
                        dict_pass[elem.get_attribute("class")] = a

        listes = [(x, y, z) for x in liste for y, z in dict_pass.items()]
        for attrib, key, value in listes:
            if int(attrib) == value:
                button = WebDriverWait(navigateur, 4).until(EC.presence_of_element_located((By.XPATH, "//button[@class='"+key+"']")))
                #print(key, value)
                button.click()

        interval_login = time.time() - start_time_login
        print('resolve pad time in seconds:',interval_login)

        #inputPostal = navigateur.find_element_by_id("champTexteCodePostal")
        inputPostal = WebDriverWait(
            navigateur, 5).until(
            EC.presence_of_element_located(
                (By.ID, "codepostal")))
        inputPostal.send_keys("78300")
        inputPostal.send_keys(Keys.RETURN)


    def deletepopup(self, navigateur):
        try:
            inputspan = WebDriverWait(navigateur, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='js-close-popin']")))
            inputspan.click()
            return True
        except:
            return False

    def cleanhtml(self, raw_html):
        raw_html = re.sub('<[^<]+?>', '', raw_html)
        raw_html = re.sub(r'\([^)]*\)', '', raw_html)
        cleantext = re.sub('(rafraîchir ce CV)', '', raw_html)
        return cleantext

    def cv(self, navigateur):
        print()
        for elem in WebDriverWait(navigateur, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//h2[@class='category-title']/a"))):
            if elem.get_attribute("innerHTML") == "Mes candidatures,<br> CV et propositions":
                print("click on '" + elem.get_attribute("innerHTML")+"' ")
                elem.click()
                break
        for elem in WebDriverWait(navigateur, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//h2[@class='category-title']/a"))):
            if elem.get_attribute("innerHTML") == "Mes <br>CV":
                print("click on '" + elem.get_attribute("innerHTML")+"' ")
                elem.click()
                break
        for i, elem in enumerate(WebDriverWait(navigateur, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//h2[@class='block-title']/a")))):
            print()
            cvspan = WebDriverWait(navigateur, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//h2[@class='block-title']/span[@class='date-refresh ng-scope']")))
            print(elem.get_attribute("innerHTML") + " ( " + self.cleanhtml(cvspan[i].get_attribute("outerHTML")).strip() + "(s) ) ")

            cvspan = WebDriverWait(navigateur, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='primary']/div[@class='parallel-unit']/span[@class='value ng-binding']")))
            print(" > " + cvspan[i].get_attribute("innerHTML"))


    def actualisation(self, navigateur):
        try:
            for elem in WebDriverWait(navigateur, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//span/a"))):
                if elem.get_attribute("innerHTML") == "Je m'actualise ?":
                    print("click on '" + elem.get_attribute("innerHTML")+"' ")
                    elem.click()
                    break
            try:
                check_actualisation = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//div[@class='parallel-unit']/div/p[2]")))
                if "Vous avez déjà déclaré votre situation pour cette période" in check_actualisation.get_attribute("innerHTML"):
                    print("Vous êtes déjà actualiser.")
                    return False
            except:
                pass

            # Etes-vous inscrit à une session de formation ou suivez-vous une formation ? 
            formationOui = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='formationOui']/strong")))
            formationNon = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='formationNon']/strong")))

            if Profile[sys.argv[2]][2] == "Oui" or Profile[sys.argv[2]][2] == "oui":
                print("Etes-vous inscrit à une session de formation ou suivez-vous une formation ? click on 'Oui'")
                formationOui.click()

            if Profile[sys.argv[2]][2] == "Non" or Profile[sys.argv[2]][2] == "non":
                print("Etes-vous inscrit à une session de formation ou suivez-vous une formation ? click on 'Non'")
                formationNon.click()

            for elem in WebDriverWait(navigateur, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//button[@class='js-only']"))):
                if elem.get_attribute("innerHTML") == "Valider":
                    elem.click()
                    break

            #Avez-vous travaillé ?
            TravailleOui = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocTravail-open']/strong")))
            TravailleNon = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocTravail-close']/strong")))

            if Profile[sys.argv[2]][3] == "Oui" or Profile[sys.argv[2]][3] == "oui":
                print("Avez-vous travaillé ? click on 'Oui'")
                TravailleOui.click()

            if Profile[sys.argv[2]][3] == "Non" or Profile[sys.argv[2]][3] == "non":
                print("Avez-vous travaillé ? click on 'Non'")
                TravailleNon.click()


            #Avez-vous été en stage ?
            StageOui = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocStage-open']/strong")))
            StageNon = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocStage-close']/strong")))

            if Profile[sys.argv[2]][4] == "Oui" or Profile[sys.argv[2]][4] == "oui":
                print("Avez-vous été en stage ? click on 'Oui'")
                StageOui.click()

            if Profile[sys.argv[2]][4] == "Non" or Profile[sys.argv[2]][4] == "non":
                print("Avez-vous été en stage ? click on 'Non'")
                StageNon.click()
           
            #Avez-vous été en arrêt maladie ?
            MaladieOui = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocMaladie-open']/strong")))
            MaladieNon = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocMaladie-close']/strong")))

            if Profile[sys.argv[2]][5] == "Oui" or Profile[sys.argv[2]][5] == "oui":
                print("Avez-vous été en arrêt maladie ? click on 'Oui'")
                MaladieOui.click()

            if Profile[sys.argv[2]][5] == "Non" or Profile[sys.argv[2]][5] == "non":
                print("Avez-vous été en arrêt maladie ? click on 'Non'")
                MaladieNon.click()
            
            #Percevez-vous une nouvelle pension retraite ?
            RetraiteOui = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocRetraite-open']/strong")))
            RetraiteNon = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocRetraite-close']/strong")))

            if Profile[sys.argv[2]][6] == "Oui" or Profile[sys.argv[2]][6] == "oui":
                print("Percevez-vous une nouvelle pension retraite ? click on 'Oui'")
                RetraiteOui.click()

            if Profile[sys.argv[2]][6] == "Non" or Profile[sys.argv[2]][6] == "non":
                print("Percevez-vous une nouvelle pension retraite ? click on 'Non'")
                RetraiteNon.click()

            #Percevez-vous une nouvelle pension d'invalidité de 2ème ou 3ème catégorie ?
            InvaliditeOui = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocInvalidite-open']/strong")))
            InvaliditeNon = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocInvalidite-close']/strong")))

            if Profile[sys.argv[2]][7] == "Oui" or Profile[sys.argv[2]][7] == "oui":
                print("Percevez-vous une nouvelle pension d'invalidité de 2ème ou 3ème catégorie ? click on 'Oui'")
                InvaliditeOui.click()

            if Profile[sys.argv[2]][7] == "Non" or Profile[sys.argv[2]][7] == "non":
                print("Percevez-vous une nouvelle pension d'invalidité de 2ème ou 3ème catégorie ? click on 'Non'")
                InvaliditeNon.click()
            

            #Etes-vous toujours à la recherche d'un emploi ?
            RechercheOui = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocRecherche-close']/strong")))
            RechercheNon = WebDriverWait(navigateur, 8).until(EC.presence_of_element_located((By.XPATH, "//label[@for='blocRecherche-open']/strong")))

            if Profile[sys.argv[2]][8] == "Oui" or Profile[sys.argv[2]][8] == "oui":
                print("Etes-vous toujours à la recherche d'un emploi ? click on 'Oui'")
                RechercheOui.click()

            if Profile[sys.argv[2]][8] == "Non" or Profile[sys.argv[2]][8] == "non":
                print("Etes-vous toujours à la recherche d'un emploi ? click on 'Non'")
                RechercheNon.click()
        except:
            return False

    def close(self, navigateur):
        navigateur.close()
        exit()

if __name__ == '__main__':
    navigateur = PoleEmplois(Profile[sys.argv[2]][0], Profile[sys.argv[2]][1], False)

