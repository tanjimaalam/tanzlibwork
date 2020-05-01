from selenium import webdriver
TRY_PAGES = 2


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
    #find_Word(' X')

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
    currentLocation = newDriver.find_element_by_class_name(
        'loc-code-global-body').text

    currentItemStatus = newDriver.find_element_by_class_name(
        'loc-status').text

    # Expand
    currentExpandAnchor = newDriver.find_element_by_class_name(
        'loc-library').find_element_by_xpath('..').find_element_by_class_name('td1').find_element_by_tag_name('a')
    currentExpandAnchor.click()
    currentBarCode = newDriver.find_element_by_xpath(
        '/html/body/table[3]/tbody/tr[11]/td[2]').text

    # go back 2 steps
    newDriver.execute_script("window.history.go(-2)")
    marcLink = newDriver.find_element_by_xpath(
        '/html/body/table[4]/tbody/tr/td/a[3]')
    marcLink.click()

    # find SYS
    """ currentSYS = newDriver.find_element_by_xpath(
        '/html/body/table[5]/tbody/tr[39]/td[2]').text """
    currentSYS = ''
    td_all = newDriver.find_elements_by_tag_name('td')
    for i in range(len(td_all)):
        if(td_all[i].text == 'SYS'):
            currentSYS = td_all[i+1].text
            break

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
            "currentBookDescription": currentBookDescription,
            "currentBarCode": str(currentBarCode),
            "currentItemStatus": currentItemStatus,
            "currentLocation": currentLocation,
            "currentSYS": str(currentSYS)
        }
    )

    newDriver.close()


def makeCSV():
    csvFile = open('./outputCSV.csv', 'a')

    for i in range(len(htmlContentInfo)):
        csvFile.write(htmlContentInfo[i]["currentSYS"] + ',')
        csvFile.write(htmlContentInfo[i]["currentCallNumber"] + ',')
        # csvFile.write(htmlContentInfo[i]["currentBookDescription"] + ',')
        csvFile.write('book name' + ',')
        csvFile.write(htmlContentInfo[i]["currentBarCode"] + ',')
        csvFile.write(htmlContentInfo[i]["currentLocation"] + ',')
        csvFile.write(htmlContentInfo[i]["currentItemStatus"] + ',')
        csvFile.write('\n')
    csvFile.close()


def makeHTML():
    bodyContent = ""
    for i in range(len(htmlContentInfo)):

        bodyContent += '<div class="infoContainer">'

        bodyContent += '<div class="callNumber">'
        bodyContent += 'Call # ' + htmlContentInfo[i]["currentCallNumber"]
        bodyContent += '</div>'

        bodyContent += '<div class="description">'
        bodyContent += 'Title: ' + htmlContentInfo[i]["currentBookDescription"]
        bodyContent += '</div>'
        bodyContent += '<div class="barcode">'
        bodyContent += 'Barcode: ' + htmlContentInfo[i]["currentBarCode"]
        bodyContent += '</div>'
        bodyContent += '<div class="location">'
        bodyContent += 'Location: ' + htmlContentInfo[i]["currentLocation"]
        bodyContent += '</div>'
        bodyContent += '<div class="item-status">'
        bodyContent += 'Item Status: ' + \
            htmlContentInfo[i]["currentItemStatus"]
        bodyContent += '</div>'
        bodyContent += '<div class="SYS">'
        bodyContent += 'SYS: ' + htmlContentInfo[i]["currentSYS"]
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
makeCSV()
