'''
This codes writes a javascript file, and was used to make part of java_functions_final.js, which was then edited further

This code opens the plots.txt file, which is a text file I made from the terminal 
that has the names of all of the files in pyplot_html_final. I then make it a string list of file names called
htmls. Then I extract the part of the html that is javascritpy and write that as a function to a javascirpt file, 
with the function name the name of the html file, and the <div id>s as the correct placeholders to correspond 
to my <div id>s in website.html
'''

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

    new_id = "'" + html[0:3] + "'" 

    javascript = javascript.replace(id, new_id)
) 
    return javascript

'''
cycle through the htmls to write a javascript file, with one function 
per figure html  
'''

for html in htmls:
    with open(html) as f: #if recreating this, will need to open html from the directory that you are reading from - was made when files in same directory 
        contents = f.read()
        code = get_code(contents, html)
        html = html[:-5]
        if code != "invalid" and "’" not in html and "." not in html and "-" not in html and "`" not in html and "&" not in html:
            print(html)  
            function = "\n function " + html + "(){" + "\n" + code + "\n }"
        output += function   

'''
Write the js file with all the plot functions. Originally written to java_functions_final.js 
''' 

with open("java_functions_final_copy.js", 'w') as f:
    f.write(output) 