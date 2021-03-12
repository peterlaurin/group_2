

with open("plots.txt","r") as myfile:
    htmls = myfile.read().split()



output = ""
def get_code(contents, html):

    '''
    Takes the figure html sting (contents) and parses it to get the javascript code with the correct id
    '''   
    try:
        divstring, rest = contents.split('<script type="text/javascript">')
    except: 
        print("can't process")
        return "invalid"
    javascript, end = rest.split("</script>")

    before, after = divstring.split("<div id=")
    id, end = after.split("class=")
    id = id.strip()

    #id to replace is first three letters of string, to indicate the correct placeholder in the website.html  
    new_id = "'" + html[0:3] + "'" #i think i need this 

    javascript = javascript.replace(id, new_id)
    #print(javascript)

    #print(id, javascript) 
    return javascript

'''
cycle through the htmls to write a javascript file, with one function 
per figure html  
'''

for html in htmls:
    #print(html)
    with open(html) as f: 
        contents = f.read()
        code = get_code(contents, html)
        #print(code)
        html = html[:-5]
        if code != "invalid" and "’" not in html and "." not in html and "-" not in html and "`" not in html and "&" not in html:
            print(html)  
            function = "\n function " + html + "(){" + "\n" + code + "\n }"
        output += function   

with open("java_functions_final.js", 'w') as f:
    f.write(output) 