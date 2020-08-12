import json
from selenium import webdriver
TRY_PAGES = 2
currentPageURL = ''

driver = webdriver.Chrome('./chromedriver/chromedriver.exe')
ccnyLibUrl = 'https://libsearch-cuny-edu.ccny-proxy1.libr.ccny.cuny.edu/F/?func=find-b-0&local_base=city'

# loading the page
driver.get(ccnyLibUrl)

# clicking the call number option in the fixed dropdown
callNumberOption = driver.find_element_by_xpath(
    '/html/body/form/table/tbody/tr/td[2]/select/option[10]')
callNumberOption.click()

# insert 61 in search field
searchBox = driver.find_element_by_xpath(
    '/html/body/form/table/tbody/tr/td[3]/input[1]')
searchBox.send_keys('61')

# initiate searching
searchButton = driver.find_element_by_xpath(
    '/html/body/form/table/tbody/tr/td[3]/input[2]')
searchButton.click()


def nextPageButton():
    img_all = driver.find_elements_by_css_selector('img')
    for i in range(len(img_all)):
        if img_all[i].get_attribute('alt') == 'Next Page':
            parent = img_all[i].find_element_by_xpath('..')
            return parent

        """ else:
            return None """


linksToBeClicked = []


def collect_links():
    global linksToBeClicked

    td1_all = driver.find_elements_by_class_name('td1')
    for i in range(len(td1_all)):
        aTags = td1_all[i].find_elements_by_css_selector('a')
        if len(aTags) != 0:
            for aTag in aTags:
                href = aTag.get_attribute('href')
                # linksToBeClicked.append(td1_all[i+1])
                linksToBeClicked.append(href)
        


pageCount = 0


def dumpIntoJson():
    # write linksToBeClicked into a file
    # with open('./output/linksToBeClicked.json', 'w+') as outfile:
    outputJSON = open('./output/linksToBeClicked.json', 'w+')
    json.dump(linksToBeClicked, outputJSON)
    outputJSON.close()


def runAutomationRecursive():
    global pageCount
    global currentPageURL
    pageCount += 1
    collect_links()

    if nextPageButton() is not None:
        # if pageCount <= TRY_PAGES:
        nextPageButton().click()
        dumpIntoJson()
        currentPageURL = driver.current_url
        print(currentPageURL)
        print('----------------------')
        runAutomationRecursive()
    else:
        print('-------The last link is just above---------------')


runAutomationRecursive()

print('successfully finished')
print('pages scraped: ')
print(pageCount)
driver.close()


htmlContentInfo = []
