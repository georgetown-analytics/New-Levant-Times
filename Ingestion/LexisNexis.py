from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from datetime import timedelta, date
import time
import random

options = webdriver.ChromeOptions()
directory = "G:\Personal\Python\Lexis Nexis Scrape"
profile = {"download.default_directory": directory}
options.add_experimental_option("prefs", profile)
browser = webdriver.Chrome(chrome_options=options)


def log_in_ln(user, passwords):
    browser.get("http://guides.library.georgetown.edu/az.php?a=l")
    seconds = 2 + (random.random() * 1)
    time.sleep(seconds)

    # Click on link to Lexis Nexis
    lexis_ready = WebDriverWait(browser, 120).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="s-lg-az-name-l"]/div[14]/div[1]/a')))
    browser.find_element_by_xpath('//*[@id="s-lg-az-name-l"]/div[14]/div[1]/a').click()
    seconds = 2 + (random.random() * 1)
    time.sleep(seconds)


    # Fill out form with Georgetown username and password to access LexisNexis
    try:
        user_name_ready = WebDriverWait(browser, 120).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="creds"]/tbody/tr[3]/td[2]/input')))
        username = browser.find_element_by_xpath('//*[@id="creds"]/tbody/tr[3]/td[2]/input')
        username.send_keys(user)
        password = browser.find_element_by_xpath('//*[@id="creds"]/tbody/tr[4]/td[2]/input')
        password.send_keys(passwords)
        seconds = 2 + (random.random() * 1)
        time.sleep(seconds)
        browser.find_element_by_xpath('//*[@id="button"]/input').click()
        seconds = 4 + (random.random() * 2)
        time.sleep(seconds)
    except NoSuchElementException:  # If you are already logged on
        seconds = 0 + (random.random() * 2)
        time.sleep(seconds)


def open_adv_options():
    # Open the advanced options by navigating to the correct frame
    try:
        seconds = 1 + (random.random() * 1)
        time.sleep(seconds)
        iframe = browser.find_elements_by_tag_name('iframe')[0]
        browser.switch_to.default_content()
        browser.switch_to.frame(iframe)
        browser.find_element_by_xpath('//*[@id="lblAdvancDwn"]').click()
        seconds = 2 + (random.random() * 1)
        time.sleep(seconds)
    except IndexError:
        browser.switch_to.default_content()
        seconds = 4 + (random.random() * 4)
        time.sleep(seconds)
        iframe = browser.find_element_by_id('mainFrame')
        browser.switch_to.default_content()
        browser.switch_to.frame(iframe)
        browser.find_element_by_xpath('//*[@id="lblAdvancDwn"]').click()
        seconds = 2 + (random.random() * 1)
        time.sleep(seconds)


def date_adv_options(start, end):
    # Select the start and end dates
    start_date = browser.find_element_by_xpath('//*[@id="txtFrmDate"]')
    start_date.send_keys(start)
    end_date = browser.find_element_by_xpath('//*[@id="txtToDate"]')
    end_date.send_keys(end)


def seg_search_adv_options(search):
    # Enter items in the "Build Your Own Segment Search" box. Ex:Headline(Congress w/5 budget)
    browser.find_element_by_xpath('//*[@id="txtSegTerms"]').clear()
    browser.find_element_by_xpath('//*[@id="txtSegTerms"]').click()
    seg_search = browser.find_element_by_xpath('//*[@id="txtSegTerms"]')
    seg_search.send_keys(search)


def content_type_adv_options(options):  # two options: newspaper, all
    option = options
    option.lower()
    # Un-select all of the options(newspaper, state and federal cases, etc) and keep just newspapers
    if option == "newspaper":
        browser.find_element_by_xpath('//*[@id="selectAll"]').click()
        browser.find_element_by_xpath('//*[@id="Newspapers"]').click()  # Clicking on newspaper
    # Keep all of the options
    if option == "all":
        pass
    if option not in ('newspaper', 'all'):
        raise Exception("Need to provide parameter: 'newspaper' or 'all'")
    seconds = 0 + (random.random() * 2)
    time.sleep(seconds)


def apply_adv_options():
    # Apply the options selected from the advanced menu
    browser.find_element_by_xpath('//*[@id="OkButt"]').click()
    # Search for the results
    browser.find_element_by_xpath('//*[@id="srchButt"]').click()
    seconds = 5 + (random.random() * 4)
    time.sleep(seconds)


def total():
    browser.switch_to.default_content()
    browser.switch_to.frame('mainFrame')
    dyn_frame = browser.find_element_by_xpath('//frame[contains(@name, "fr_resultsNav")]')
    framename = dyn_frame.get_attribute('name')
    browser.switch_to.frame(framename)
    total = int(browser.find_element_by_name('totalDocsInResult').get_attribute('value'))
    browser.switch_to.default_content()
    return total


def click_download():
    # Navigates to the frame that contains the download button and clicks button to open download window
    browser.switch_to.default_content()
    browser.switch_to.frame('mainFrame')
    dyn_frame = browser.find_element_by_xpath('//frame[contains(@name, "fr_resultsNav")]')
    framename = dyn_frame.get_attribute('name')
    browser.switch_to.frame(framename)
    browser.find_element_by_xpath('//*[@id="deliveryContainer"]/table/tbody/tr/td[6]/table/tbody/tr/td[1]/table/'
                                  'tbody/tr/td/a[3]/img').click()
    seconds = 1 + (random.random() * 1)
    time.sleep(seconds)


def navigate_download_window():
    # Navigate to the opened download window
    try:
        browser.switch_to.window(browser.window_handles[1])
    except IndexError:
        time.sleep(10)
        browser.switch_to.window(browser.window_handles[1])


def download_select_item():
    # Navigate to select item box
    try:
        browser.find_element_by_id('rangetextbox').clear()
        browser.find_element_by_id('rangetextbox').send_keys('{}-{}'.format(initial, final))
        browser.find_element_by_css_selector('img[alt=\"Send\"]').click()
    except NoSuchElementException:
        pass


def download_format(format):
    # Select the format type
    if format == "Word":
        formats = str(1)
    if format == "HTML":
        formats = str(2)
    if format == "Generic":
        formats = str(3)
    if format == "Text":
        formats = str(4)
    if format == "PDF":
        formats = str(5)
    if format == "Excel":
        formats = str(6)
    if format not in ('Word', 'HTML', 'Generic', 'Text', 'PDF', 'Excel'):
        raise Exception('Option not valid. Select one of six options found in format drop down menu: '
                        'Word, HTML, Generic, Text, PDF, Excel')

    browser.find_element_by_xpath('//*[@id="delFmt"]/option[' + formats + ']').click()
    seconds = 1 + (random.random() * 1)
    time.sleep(seconds)
    # Clicks the download button in the download window
    browser.find_element_by_xpath('//*[@id="img_orig_bottom"]/a/img').click()


def download_files(file_extension):
    # Select the format type
    if file_extension == "Word":
        extension = '.DOC'
    if file_extension == "HTML":
        extension = '.HTML'
    if file_extension == "Generic":
        extension = '.RTF'
    if file_extension == "Text":
        extension = '.TXT'
    if file_extension == "PDF":
        extension = '.PDF'
    if file_extension == "Excel":
        extension = '.CSV'
    if file_extension not in ('Word', 'HTML', 'Generic', 'Text', 'PDF', 'Excel'):
        raise Exception('Option not valid. Select one of six options found in format drop down menu: '
                        'Word, HTML, Generic, Text, PDF, Excel')
    try:
        download_button = WebDriverWait(browser, 120).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, extension)))
        browser.find_element_by_partial_link_text(extension).click()
    except TimeoutException:
        time.sleep(30)
        browser.find_element_by_partial_link_text(extension).click()
    except NoSuchElementException:
        time.sleep(30)
        browser.find_element_by_partial_link_text(extension).click()
    seconds = 4 + (random.random() * 5)
    time.sleep(seconds)
    close_window = WebDriverWait(browser, 120).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="center"]/div/p[4]/a/img')))
    browser.find_element_by_xpath('//*[@id="center"]/div/p[4]/a/img').click()
    seconds = 1 + (random.random() * 4)
    time.sleep(seconds)
    browser.switch_to.window(lnacademic)

if __name__ == "__main__":
    log_in_ln("*Username*", "*Password*")
    for year in range(2011, 2017):
        for month in range(1, 13):
            print "Year:", year, "Month:", month
            start_date = date(year, month, 1)
            end_date = date(year+1, 1, 1)

            lnacademic = browser.window_handles[0]

            open_adv_options()
            date_adv_options(start_date.strftime("%Y/%m/%d"), end_date.strftime("%Y/%m/%d"))
            seg_search_adv_options("((Syria!) and ((#STX001346#) AND (#STX000752#) AND (#ST00098A0#) AND (#STX000950#))")
            content_type_adv_options("newspaper")
            apply_adv_options()

            total()
            print "    TOTAL:", total()
            # There is a 500 item limit per download. If there are less than 500 items, after the download you proceed
            # to the next date, if not you download in increments of 500 until all of the items are downloaded
            if total()<500:
                click_download()
                navigate_download_window()
                download_format("Text")

                download_files("Text")
                time.sleep(1)
                browser.switch_to.default_content()
                browser.find_element_by_xpath('//*[@id="logo_img"]/a').click()
            try:
                if total()>500:
                    initial = 1
                    final = 500
                    batch = 0
                    while final <= total() and final >= initial:
                        batch += 1
                        click_download()
                        navigate_download_window()
                        download_select_item()
                        download_format("Text")

                        download_files("Text")
                        initial += 500
                        if final + 500 > total():
                            final = total()
                        else:
                            final += 500
                    time.sleep(1)
                    browser.switch_to.default_content()
                    browser.find_element_by_xpath('//*[@id="logo_img"]/a').click()
            except WebDriverException:
                continue
    print "**Finished Download Successfully**"
