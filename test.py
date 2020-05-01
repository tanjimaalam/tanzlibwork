#textFile = open("sample.txt", "w")
headerFile = open("./templates/header.txt", "r")
footerFile = open('./templates/footer.txt', 'r')
headerContent = headerFile.read()
footerContent = footerFile.read()

bodyContent = '''
    <h1>hello world</h1>
    <h2>mello worlddddddddddddd</h2>
'''


fileContent = headerContent + bodyContent + footerContent

outputHTML = open('./templates/output.html', 'w+')
outputHTML.write(fileContent)

outputHTML.close()
headerFile.close()
footerFile.close()
