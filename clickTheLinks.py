from selenium import webdriver
import json

with open('./output/linksToBeClicked.json') as json_file:
    linksToBeClicked = json.load(json_file)


htmlContentInfo = []


def makeCSV():
    delimeter = ','
    csvFile = open('./outputCSV.csv', 'w+')
    csvFile.write(
        f'''"Syst. No"{delimeter} "Call #	"{delimeter} "Title"{delimeter} "Barcode"{delimeter} "Location"{delimeter} "Item Status"{delimeter}''')
    csvFile.write('\n')

    for i in range(len(htmlContentInfo)):
        csvFile.write(htmlContentInfo[i]["currentSYS"] + delimeter)
        csvFile.write(htmlContentInfo[i]["currentCallNumber"] + delimeter)
        csvFile.write(htmlContentInfo[i]["currentBookTitle"] + delimeter)
        # csvFile.write('book name' + ',')
        csvFile.write(htmlContentInfo[i]["currentBarCode"] + delimeter)
        csvFile.write(htmlContentInfo[i]["currentLocation"] + delimeter)
        csvFile.write(htmlContentInfo[i]["currentItemStatus"] + delimeter)
        csvFile.write('\n')
    csvFile.close()


# open links and find location and call number
for i in range(len(linksToBeClicked)):
    print(linksToBeClicked[i])
    newDriver = webdriver.Chrome()
    newDriver.get(linksToBeClicked[i])

    # currentBookTitle = newDriver.find_element_by_id('bib-detail').text
    currentBookTitleWithComma = newDriver.find_element_by_xpath(
        '/html/body/table[5]/tbody/tr[3]/td[2]/a').text
    currentBookTitle = currentBookTitleWithComma.replace(',', ';')

    loc_callNum_link = newDriver.find_element_by_class_name(
        'button-link').find_element_by_xpath('..')
    loc_callNum_link.click()

    currentCallNumber = (newDriver.find_element_by_class_name(
        'loc-call-number').text).replace(',', ';')
    currentLocation = (newDriver.find_element_by_class_name(
        'loc-code-global-body').text).replace(',', ';')

    currentItemStatus = (newDriver.find_element_by_class_name(
        'loc-status').text).replace(',', ';')

    # Expand
    currentExpandAnchor = newDriver.find_element_by_class_name(
        'loc-library').find_element_by_xpath('..').find_element_by_class_name('td1').find_element_by_tag_name('a')
    currentExpandAnchor.click()
    currentBarCode = (newDriver.find_element_by_xpath(
        '/html/body/table[3]/tbody/tr[11]/td[2]').text).replace(',', ';')

    # go back 2 steps
    newDriver.execute_script("window.history.go(-2)")
    marcLink = newDriver.find_element_by_xpath(
        '/html/body/table[4]/tbody/tr/td/a[3]')
    marcLink.click()

    # find SYS
    currentSYS = ''
    td_all = newDriver.find_elements_by_tag_name('td')
    for i in range(len(td_all)):
        if(td_all[i].text == 'SYS'):
            currentSYS = td_all[i+1].text
            break

    htmlContentInfo.append(
        {
            "currentCallNumber": currentCallNumber,
            # "currentBookTitle": currentBookTitle,
            "currentBookTitle": str(currentBookTitle),
            "currentBarCode": str(currentBarCode),
            "currentItemStatus": currentItemStatus,
            "currentLocation": currentLocation,
            "currentSYS": str(currentSYS)
        }
    )

    makeCSV()

    newDriver.close()
