from unicodedata import normalize
from py_fumen_py import decode as pydecode, encode as pyencode, Field, Page
import os

#took me like 45 minutes to code, 1:30 to debug
#overkill decode and encode stuff
def encode(text):
  text = '\n'.join(text[i:i + 10] for i in range(0, len(text), 10))
  tetrisfield = Field(field=text, garbage="__________")
  page = Page(field=tetrisfield)
  return (pyencode([page]))

def decode(fumen):
  decode_pages = pydecode(fumen)
  return colorize_text('\n'.join(decode_pages[0].field.string().splitlines()[:-1]))

def texttofumen(text):
  return encode(text.replace("\n", ""))
  
def colorize_text(text):
    color_mapping = {
        '_': '\u001b[30m',  # Black
        'X': '\u001b[90m',  # Gray
        'S': '\u001b[92m',  # Green
        'J': '\u001b[94m',  # Blue
        'L': '\u001b[33m',  # Orange
        'Z': '\u001b[31m',  # Red
        'I': '\u001b[96m',  # Light Blue
        'O': '\u001b[93m',  # Yellow
        'T': '\u001b[95m'   # Purple
    }
        

    colored_text = ""
    for char in text:
        if char in ['X','R','S','J','L','Z','I','O','T','_']:
            colored_text += color_mapping.get(char, '') + '██' + '\u001b[0m'
        elif char == '_':
            colored_text += color_mapping.get(char, '') + '  ' + '\u001b[0m'
        else:
            colored_text += color_mapping.get(char, '') + char + '\u001b[0m'
    
    return colored_text

def split_fumen(fumen: str) -> list[str]:
    '''
    Splits a fumen into each of its pages

    Parameter:
        fumen (str): a fumen code

    Return:
        list[str]: a list of each of the fumens
    '''

    # fumen output 
    splitted_fumens = []

    try:
        pages = pydecode(fumen)
    except:
        raise RuntimeError(f"Fumen {fumen} could not be decoded")

    # go through page
    for page in pages:
        # encode the page as a new fumen
        fumen_of_page = pyencode([page])

        # add to list of fumens
        splitted_fumens.append(fumen_of_page)

    return splitted_fumens
    
#read file contents
file = open("path_minimal_strict.md", "r", encoding='utf-8')
Content = file.read()
count = Content.split("\n")[1]
percent = Content.split("Success rate: ",1)[1]
percent = "Success rate: " + percent.split("\n",1)[0]
block = Content.split("### Details")[0]
block = block.split("### Summary")[1]
block = block.replace("\n","").replace("[fumen image]","")
block = block.split(" ")
os.system("")
print(count)
print(percent)
counter = 0
fumens = ""
for i in block:
    counter = counter + 1
    text = ""
    pure = i.replace(")","").split("https://harddrop.com/fumen/?")[1]
    fumenList = split_fumen(pure)
    if len(fumenList) > 1:
        concatFumen = ""
        for i in fumenList:
            concatFumen = concatFumen + "\n" + i
        text = text + "Solution fumens "  + str(counter) + concatFumen
    else:
        text = text + "Solution fumen "  + str(counter) + "\n" + pure
    for i in fumenList:
        fumens = fumens + i + "\n"
        text = text + "\n\n" + decode(i)
    print(text)
print("Just the fumens:")
print(fumens)