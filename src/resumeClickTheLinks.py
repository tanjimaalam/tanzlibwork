from selenium import webdriver
import json

# with open('./output/linksToBeClicked.json') as json_file:
json_file = open('./output/linksToBeClicked.json', 'r')
linksToBeClicked = json.load(json_file)

lsatLink = input(''' 
    oooooooooooooooooooooooo
      Last Oversized link?
    oooooooooooooooooooooooo

''')


def getLastLinkIndexInJSON(linksToBeClicked):
    for i in range(len(linksToBeClicked)):
        if linksToBeClicked[i] == lsatLink:
            return i


htmlContentInfo = []


def appendToCSV():
    delimeter = ','
    csvFile = open('./output/outputCSV.csv', 'a')

    for j in range(len(htmlContentInfo)):
        csvFile.write(htmlContentInfo[j]["currentSYS"] + delimeter)
        csvFile.write(htmlContentInfo[j]["currentCallNumber"] + delimeter)
        csvFile.write(htmlContentInfo[j]["currentBookTitle"] + delimeter)
        # csvFile.write('book name' + ',')
        csvFile.write(htmlContentInfo[j]["currentBarCode"] + delimeter)
        csvFile.write(htmlContentInfo[j]["currentLocation"] + delimeter)
        csvFile.write(htmlContentInfo[j]["currentItemStatus"] + delimeter)
        csvFile.write(htmlContentInfo[j]["currentStatusField"] + delimeter)
        csvFile.write('\n')
    csvFile.close()


# open links and find location and call number
lastLinkIndex = getLastLinkIndexInJSON(linksToBeClicked)
for i in range(len(linksToBeClicked))[lastLinkIndex: len(linksToBeClicked)]:

    print('')
    print('-------- getting info from -------------')
    print(linksToBeClicked[i])
    print('')

    newDriver = webdriver.Chrome()
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
    currentExpandAnchor = newDriver.find_element_by_class_name(
        'loc-library').find_element_by_xpath('..').find_element_by_class_name('td1').find_element_by_tag_name('a')
    currentExpandAnchor.click()

    currentBarCode = "None"
    td_all = newDriver.find_elements_by_tag_name('td')
    for i in range(len(td_all)):
        if "Barcode" in td_all[i].text:
            currentBarCode = (td_all[i+1].text).replace(',', ';')

    # go back 2 steps
    newDriver.execute_script("window.history.go(-2)")

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

    appendToCSV()
    newDriver.close()


# print success or failure
print('''
ooooooooooooooooooooooooooooooo
If you see no errors above, then bingo!
Find the outputCSV.csv file in the output folder.

If there were errors, then run: 

      python ./src/resumeClickTheLinks.py

and copy-paste the last link found a bit upstairs.
ooooooooooooooooooooooooooooooo

''')
