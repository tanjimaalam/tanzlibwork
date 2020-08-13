from selenium import webdriver
import json

# with open('./output/linksToBeClicked.json') as json_file:
json_file = open('./output/linksToBeClicked.json', 'r')
linksToBeClicked = json.load(json_file)


htmlContentInfo = []


def makeCSV():
    delimeter = ','
    csvFile = open('./output/outputCSV.csv', 'w+', encoding="utf-8")
    csvFile.write(
        f'''"Syst. No"{delimeter} "Call #	"{delimeter} "Title"{delimeter} "Barcode"{delimeter} "Location"{delimeter} "Item Status"{delimeter} "Status Field"{delimeter}''')
    csvFile.write('\n')

    for i in range(len(htmlContentInfo)):
        csvFile.write(htmlContentInfo[i]["currentSYS"] + delimeter)
        csvFile.write(htmlContentInfo[i]["currentCallNumber"] + delimeter)
        csvFile.write(htmlContentInfo[i]["currentBookTitle"] + delimeter)
        # csvFile.write('book name' + ',')
        csvFile.write(htmlContentInfo[i]["currentBarCode"] + delimeter)
        csvFile.write(htmlContentInfo[i]["currentLocation"] + delimeter)
        csvFile.write(htmlContentInfo[i]["currentItemStatus"] + delimeter)
        csvFile.write(htmlContentInfo[i]["currentStatusField"] + delimeter)
        csvFile.write('\n')
    csvFile.close()


# open links and find location and call number
for i in range(len(linksToBeClicked)):

    print('')
    print('-------- getting info from -------------')
    print(linksToBeClicked[i])
    print('')

    newDriver = webdriver.Chrome('./chromedriver/chromedriver.exe')
    newDriver.get(linksToBeClicked[i])

    td_all = newDriver.find_elements_by_tag_name('td')
    for i in range(len(td_all)):
        if "Title" in td_all[i].text:
            print(td_all[i+1].text)
            currentBookTitle = (td_all[i+1].text).replace(',', ';')

    loc_callNum_link = newDriver.find_element_by_class_name(
        'button-link').find_element_by_xpath('..')  # this is an <a> tag
    loc_callNum_link.click()

    currentCallNumber = (newDriver.find_element_by_class_name(
        'loc-call-number').text).replace(',', ';')
    currentLocation = (newDriver.find_element_by_class_name(
        'loc-code-global-body').text).replace(',', ';')

    currentItemStatus = (newDriver.find_element_by_class_name(
        'loc-status').text).replace(',', ';')

    # Expand
    expandAnchorLinks = []
    a_all = newDriver.find_elements_by_css_selector('a')
    for a in a_all:
        if a.text == 'Expand':
            expandAnchorLinks.append(a.get_attribute('href'))

    currentBarCodes = []
    for expandLink in expandAnchorLinks:
        # expandLink.click()
        expandLinkDriver = webdriver.Chrome('./chromedriver/chromedriver.exe')
        expandLinkDriver.get(expandLink)

        #currentExpandAnchor = newDriver.find_element_by_class_name('loc-library').find_element_by_xpath('..').find_element_by_class_name('td1').find_element_by_tag_name('a')
        # currentExpandAnchor.click()

        currentBarCode = "None"
        td_all = expandLinkDriver.find_elements_by_tag_name('td')
        for i in range(len(td_all)):
            if "Barcode" in td_all[i].text:
                currentBarCode = (td_all[i+1].text).replace(',', ';')
                currentBarCodes.append(currentBarCode)

        expandLinkDriver.close()

    # go back 1 steps
    newDriver.execute_script("window.history.go(-1)")

    aTag_all = newDriver.find_elements_by_tag_name('a')
    for i in range(len(aTag_all)):
        if "MARC" in aTag_all[i].text:
            marcLink = aTag_all[i]
            break

    marcLink.click()

    # find SYS
    currentSYS = 'None'
    td_all = newDriver.find_elements_by_tag_name('td')
    for i in range(len(td_all)):
        if(td_all[i].text == 'SYS'):
            currentSYS = td_all[i+1].text
            break

    aTag_all = newDriver.find_elements_by_tag_name('a')
    for i in range(len(aTag_all)):
        if "Labels" in aTag_all[i].text:
            labelsLink = aTag_all[i]
            break

    labelsLink.click()

    currentStatusField = 'None'
    td_all = newDriver.find_elements_by_tag_name('td')
    for i in range(len(td_all)):
        if(td_all[i].text == 'Status Field'):
            currentStatusField = td_all[i+1].text
            break

    for currentBarCode in currentBarCodes:
        htmlContentInfo.append(
            {
                "currentCallNumber": currentCallNumber,
                # "currentBookTitle": currentBookTitle,
                "currentBookTitle": str(currentBookTitle),
                "currentBarCode": str(currentBarCode),
                "currentItemStatus": currentItemStatus,
                "currentLocation": currentLocation,
                "currentSYS": str(currentSYS),
                "currentStatusField": currentStatusField
            }
        )

    makeCSV()
    newDriver.close()


# print success or failure
print('''
ooooooooooooooooooooooooooooooo
If you see no errors above, then bingo!
Find the outputCSV.csv file in the output folder.

If there were errors, then :'(
Run again by pressing <Up Arrow> and then <Enter>
ooooooooooooooooooooooooooooooo

''')
