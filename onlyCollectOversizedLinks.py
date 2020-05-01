import json
from selenium import webdriver
TRY_PAGES = 2
currentPageURL = ''

driver = webdriver.Chrome()
ccnyLibUrl = 'https://libsearch-cuny-edu.ccny-proxy1.libr.ccny.cuny.edu/F/?func=find-b-0&local_base=city&fbclid=IwAR1WZIh0tPZIzKOOTEI4tHCH_7_vNNeLL8jElor7z7kcwj7hgUKlKCOneBQ'

# loading the page
driver.get(ccnyLibUrl)

# clicking the call number option in the fixed dropdown
callNumberOption = driver.find_element_by_xpath(
    '/html/body/form/table/tbody/tr/td[2]/select/option[10]')
callNumberOption.click()

# insert ML in search field
searchBox = driver.find_element_by_xpath(
    '/html/body/form/table/tbody/tr/td[3]/input[1]')
searchBox.send_keys('ML')

# initiate searching
searchButton = driver.find_element_by_xpath(
    '/html/body/form/table/tbody/tr/td[3]/input[2]')
searchButton.click()


def nextPageButton():
    img_all = driver.find_elements_by_tag_name('img')
    for i in range(len(img_all)):
        if img_all[i].get_attribute('alt') == 'Next Page':
            parent = img_all[i].find_element_by_xpath('..')
            return parent

        """ else:
            return None """


linksToBeClicked = []


def find_Word(word):
    global linksToBeClicked

    td1_all = driver.find_elements_by_class_name('td1')
    for i in range(len(td1_all)):
        if(td1_all[i].text.find(word) != -1):
            href = td1_all[i +
                           1].find_element_by_tag_name('a').get_attribute('href')
            # linksToBeClicked.append(td1_all[i+1])

            linksToBeClicked.append(href)


pageCount = 0


def dumpIntoJson():
    # write linksToBeClicked into a file
    with open('./output/linksToBeClicked.json', 'w+') as outfile:
        json.dump(linksToBeClicked, outfile)
        outfile.close()


def runAutomationRecursive():
    global pageCount
    global currentPageURL
    pageCount += 1
    find_Word('Oversize')
    #find_Word(' X')

    if nextPageButton() is not None:
        # if pageCount <= TRY_PAGES:
        nextPageButton().click()
        dumpIntoJson()
        currentPageURL = driver.current_url
        print(currentPageURL)
        print('----------------------')
        runAutomationRecursive()
    else:
        print('----------------------')


runAutomationRecursive()

print('successfully finished')
print('pages scraped: ')
print(pageCount)
driver.close()


htmlContentInfo = []
