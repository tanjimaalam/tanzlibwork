from selenium import webdriver
TRY_PAGES = 20


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


def runAutomationRecursive():
    global pageCount
    pageCount += 1
    find_Word('Oversize')
    find_Word(' X')

    print(nextPageButton())

    # if nextPageButton() is not None:
    if pageCount <= TRY_PAGES:
        nextPageButton().click()
        runAutomationRecursive()
    else:
        print('----------------------')


runAutomationRecursive()

print('successfully finished')
print('pages scraped: ')
print(pageCount)
driver.close()


htmlContentInfo = []

# open links and find location and call number
for i in range(len(linksToBeClicked)):
    print(linksToBeClicked[i])
    newDriver = webdriver.Chrome()
    newDriver.get(linksToBeClicked[i])

    loc_callNum_link = newDriver.find_element_by_class_name(
        'button-link').find_element_by_xpath('..')
    loc_callNum_link.click()

    currentCallNumber = newDriver.find_element_by_class_name(
        'loc-call-number').text
    currentBookDescription = newDriver.find_element_by_id('bib-detail').text

    callNumbersTXT = open('callNumbers.txt', "w")
    callNumbersTXT.write(currentCallNumber)
    callNumbersTXT.write('\n')
    callNumbersTXT.write(currentBookDescription)
    callNumbersTXT.write('\n')
    callNumbersTXT.write('------')
    callNumbersTXT.write('\n')

    htmlContentInfo.append(
        {
            "currentCallNumber": currentCallNumber,
            "currentBookDescription": currentBookDescription
        }
    )

    newDriver.close()


def makeHTML():
    bodyContent = ""
    for i in range(len(htmlContentInfo)):

        bodyContent += '<div class="infoContainer">'
        bodyContent += '<div class="callNumber">'
        bodyContent += htmlContentInfo[i]["currentCallNumber"]
        bodyContent += '</div>'

        bodyContent += '<div class="description">'
        bodyContent += htmlContentInfo[i]["currentBookDescription"]
        bodyContent += '</div>'
        bodyContent += '</div>'

    headerFile = open("./templates/header.txt", "r")
    footerFile = open('./templates/footer.txt', 'r')
    headerContent = headerFile.read()
    footerContent = footerFile.read()

    outputFileContent = headerContent + bodyContent + footerContent
    outputHTML = open('output.html', 'w+')
    outputHTML.write(outputFileContent)
    outputHTML.close()


makeHTML()
