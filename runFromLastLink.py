import json
from selenium import webdriver
TRY_PAGES = 2
currentPageURL = ''

driver = webdriver.Chrome()
lastLink = 'https://libsearch-cuny-edu.ccny-proxy1.libr.ccny.cuny.edu/F/IUEJYTKRKEGK748D48PYP19JG436QUNIVK6GBMK614S6DQ7LX5-14512?func=scan-ind-continue&code=SHL&find_scan_code=SCAN_SHL&filing_text=ml%22172%20c86%20x%20oversize%200&sequence=001116399'
driver.get(lastLink)

linksToBeClicked = []
with open('./temp/linksToBeClicked.json') as json_file:
    linksToBeClicked = json.load(json_file)


def nextPageButton():
    img_all = driver.find_elements_by_tag_name('img')
    for i in range(len(img_all)):
        if img_all[i].get_attribute('alt') == 'Next Page':
            parent = img_all[i].find_element_by_xpath('..')
            return parent

        """ else:
            return None """


def find_Word(word):
    global linksToBeClicked

    td1_all = driver.find_elements_by_class_name('td1')
    for i in range(len(td1_all)):
        if(td1_all[i].text.find(word) != -1):
            href = td1_all[i +
                           1].find_element_by_tag_name('a').get_attribute('href')
            textFile = open("sample.txt", "a")
            textFile.write(td1_all[i].text)
            textFile.write('\n')
            textFile.write(td1_all[i+1].text)
            textFile.write('\n')
            textFile.write(href)
            textFile.write('\n')
            textFile.write("-----------")
            textFile.write('\n')
            textFile.close()

            # linksToBeClicked.append(td1_all[i+1])

            linksToBeClicked.append(href)


pageCount = 0


def dumpIntoJson():
    # write linksToBeClicked into a file
    with open('./temp/linksToBeClicked.json', 'w+') as outfile:
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
