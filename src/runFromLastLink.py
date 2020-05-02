import json
from selenium import webdriver
TRY_PAGES = 2
currentPageURL = ''

driver = webdriver.Chrome()
#lastLink = 'https://libsearch-cuny-edu.ccny-proxy1.libr.ccny.cuny.edu/F/LYUHLKB86T9RK5AI6P5LRJQVXL7K7ARVVEY8FBARB8TB97BRBH-07753?func=scan-ind-continue&code=SHL&find_scan_code=SCAN_SHL&filing_text=ml%2128%20n5%20n384%202010&sequence=007046408'

askLastLink = '''
oooooooooooooooooooooooooooooooooooooooooooooo
Paste the last link traversed and press Enter.
oooooooooooooooooooooooooooooooooooooooooooooo

'''
lastLink = input(askLastLink)
driver.get(lastLink)

linksToBeClicked = []
# with open('./output/linksToBeClicked.json') as json_file:
json_file = open('./output/linksToBeClicked.json', 'r')
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

            # linksToBeClicked.append(td1_all[i+1])

            linksToBeClicked.append(href)


pageCount = 0


def dumpIntoJson():
    # write linksToBeClicked into a file
    # with open('./output/linksToBeClicked.json', 'w+') as outfile:
    outfile = open('./output/linksToBeClicked.json', 'w+')
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
        print('-------The last link is just above---------------')


runAutomationRecursive()

print('successfully finished')
print('pages scraped: ')
print(pageCount)
driver.close()
