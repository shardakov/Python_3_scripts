import requests

URL = "https://translate.yandex.net/api/v1.5/tr.json/translate" 
# Your api key
KEY = "trnsl.1.1.20190429T065522Z.18f4830c20ee2f4b.b940037513ea0a3e99dd7129948c0a456985e3d6b"

text_input = r'1.txt'
text_output = r'2.txt'
text_ru = r'3.txt'

def rep_pdf_to_txt(text_in, text_out):
  with open(text_input, 'r') as f1, open(text_output, 'w') as f2:
    lines = f1.readlines()
    for line in lines:
        if(line.endswith(".\n")):
            f2.write(line + "\n")
        else:
            f2.write(line.replace("\n", " ") + " ")

def split_text(text_out):
  with open(text_output, 'r') as f2:
    tmp_text = f2.read()
    tmp = tmp_text.split(".")
    n = 0
    tmp_str = ""
    tmp_list = []
    for str in tmp:
      n += len(str)
      tmp_str += str + "."
      if(n > 9000):  
        tmp_list.append(tmp_str)
        tmp_str = ""
        n = 0
    return tmp_list

def translate(my_text):
  params = {
    "key": KEY,
    "text": my_text,    
    "lang": 'en-ru'
  }
  response = requests.get(URL, params = params)
  json_response = response.json()
  return json_response

# input parameters
'''
my_text = "Test params for my text input for translate"
json = translate(my_text)
print(''.join(json["text"]))
'''
rep_pdf_to_txt(text_input, text_output)
t_list = split_text(text_output)
with open(text_ru, 'w') as f3:
  for i in t_list:
    f3.write(''.join(translate(i)["text"]))
    f3.write("\n Переведено сервисом «Яндекс.Переводчик»  http://translate.yandex.ru/ \n")