input_text = "test.txt"
output = "imagePts.xml"
values = []
xml = ""

N = sum(1 for line in open('test.txt'))

if N % 4 is not 0:
    print("Ooops!, Check input values")
else:
    xml += "<opencv_storage>\n  <imagePts>"
    i = 1
    with open(input_text, "r") as file:
        for c in file:
            values.append(c.split(" ")[0])
            values.append(c.split(" ")[1])
            if i % 4 is 0:
                xml += "\n    <_><_>\n        " + str(float(values[0])) + " "+str(float(values[1])) + \
                       "</_>\n      <_>\n       " + " " + str(float(values[2])) + " " + str(float(values[3])) + \
                       "</_>\n      <_>\n        " + str(float(values[4])) + " " + str(float(values[5])) + \
                       "</_>\n      <_>\n        " + str(float(values[6])) + " " + str(float(values[7])) + \
                       "</_></_>"
                values.clear()
            i += 1
    xml += "\n  </imagePts>\n</opencv_storage>"

    o = open(output, "w+")
    o.write(xml)
    print("Converting values to XML Finished.")
