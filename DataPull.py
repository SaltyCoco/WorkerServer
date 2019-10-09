import time
import os
import datetime as dt
from Props import Props_var
from datetime import date, timedelta
from time import strftime as st
from DMS.DMSemFileUL import etl_ulDMS
from selenium import webdriver
from fileMGNT.fileMGNT import CleanDLF_CSV, moveDLcsv, dataETL, LA_dataETL, FA_dataETL
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def CleanDLF_CSV(title,folder):
    print(title + ' Initiated downloads cleared')
    for the_file in os.listdir(folder):
      file_path = os.path.join(folder, the_file)
      try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
      except Exception as e:
        print(e)
    time.sleep(1)
    print(title + ' Completed: downloads cleared')

def dataExt(turl):
    props = Props_var()
    crmUS = props.crmUS
    crmPS = props.crmPS
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browse.download.dir", '<path to directory>')
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(
        executable_path=r'<path to geckodriver.exe>',
        firefox_profile=fp, firefox_options=options)
    crmUrl = '<crmURL>'
    driver.get(crmUrl)
    # this walks through the DOM for login.  It would likely be different an alternitve site
    WebDriverWait(driver, 100).until(
        lambda driver: driver.find_element_by_id('maincontent_Username'))
    driver.find_element_by_id('maincontent_Username').send_keys("username")
    driver.find_element_by_id('maincontent_Password').send_keys("password")
    driver.find_element_by_id('maincontent_LoginButton').click()
    WebDriverWait(driver, 100).until(
        lambda driver: driver.find_element_by_id('maincontent_Login'))
    driver.find_element_by_id('maincontent_Login').click()

     # AppServer
    asFDgen = '<Path to raw>'
    # Local
    #asFDgen = '<path to test>'
    asFDcustVerifi = '<path to test>'
    DLF = '<path to download file>'
    for reps in turl:
        #Report pull 1
        elif reps == 'rep1':
            try:
                url = '<url>'
                    print('initiating rep1 DL')
                    mn = st("%m")
                    yr = st("%Y")
                    ds = str(mn + "/" + "01" + "/" + yr)
                    driver.get(url)
                    time.sleep(10)
                    WebDriverWait(driver, 100).until(
                        lambda driver: driver.find_element_by_id('maincontent_From_Date'))
                    driver.find_element_by_id('maincontent_Date_From').click()
                    driver.find_element_by_id('maincontent_Date_From').clear()
                    driver.find_element_by_id('maincontent_Date_From').send_keys(ds)
                    time.sleep(3)
                    driver.find_element_by_id('maincontent_Export').click()
                    print('rep1 completed')
                    time.sleep(10)
                    fn = asFDgen + 'rep1.csv'
                    moveDLcsv(title='rep1 Raw DL', MDL_newFileName=fn, DLF=DLF)
                try:
                    # this def basically aggrigates the data and appends it to a database
                    dataETL('FA', fn, fn)
                except Exception as e:
                    print('etl failed ' + str(e))

                print('completed mal')
            except Exception as e:
                print('FAILED capp ' + str(e))

        #Report pull 2 using lambdas
        elif reps == 'rep2':
            try:
                url = '<url>'
                print('initiating cal DL')
                fn = asFDgen + 'rep2.csv'
                driver.get(url)
                time.sleep(10)
                WebDriverWait(driver, 100).until(
                    lambda driver: driver.find_element_by_id('maincontent_Export'))
                driver.find_element_by_id('maincontent_Export').click()
                time.sleep(10)
                print('rep2 DL completed')
                moveDLcsv(title='rep 2 Raw DL', MDL_newFileName=fn, DLF=DLF)
                print('initiating rep etl')
                dataETL('std', fn, fn)
                print('completed rep 2')
            except Exception as e:
                print('FAILED rep 2 ' + e)            

        elif reps == 'exit':
                try:
                    driver.quit()
                    print('successfully exit driver')
                except Exception as e:
                    print('failed to exit driver')
                    print(e)

        else:
            print('Incorrent v parameter')
            
    print('completed all data loads')
    try:
        driver.quit()
    except Exception as e:
        print(e)
    print('Said goodbye to selenium and gecko')