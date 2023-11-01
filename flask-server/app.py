import io
from PIL import Image
from pyclovaocr import ClovaOCR
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import openai
import os
import json
from konlpy.tag import Okt
import json
import os
okt = Okt()
# import pymysql
# with open('./secret.json') as f:
#     secrets = json.loads(f.read())

# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets[setting]
#     except KeyError:
#         error_msg = "Set the {} environment variable".format(setting)
#         return (error_msg)

openai.api_key = "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"

# db = pymysql.connect(host='svc.sel3.cloudtype.app',
#                      port=30616,
#                      user='root',
#                      passwd='mysql',
#                      db='swdc',
#                      charset='utf8')

# try:
#     with db.cursor() as cursor:
#         sql = """
#                 CREATE TABLE (
#                    word  VARCHAR(256) NOT NULL PRIMARY KEY,
#                    simi_words VARCHAR(256) NOT NULL,
#                 );
#               """
#         cursor.execute(sql)
#         db.commit()
# finally:
#     pass

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
ocr = ClovaOCR()

def process_ocr(base64_image):
    image_bytes = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_bytes))
    
    image.save('temp_image.png')
    
    result = ocr.run_ocr(
    image_path='temp_image.png',
    language_code='ko',
    ocr_mode='general'
    )
    return result



def gpt_response_sim_word(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= 
        [
            
            {
                "role": "system",
                "content": "너는 출력할 때 이 출력형식을 따라야해 다른 문자는 절대 보낼 수 없어 '유의어1 유의어2 유의어3' 내가 말한 단어의 유의어 3가지를 띄어쓰기로 구분해서 알려줘"
            },
            {
            "role": "user",
            "content": "사랑"
            },
            {
            "role": "assistant",
            "content": "마음 심신 정"
            },
            {
            "role": "user",
            "content": "위로"
            },
            {
            "role": "assistant",
            "content": "위안 사과 안락"
            },
            {
                "role":"user",
                "content": text
            }
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['message']['content']



def gpt_response(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "어려운 단어를 쉬운 단어로 바꿔 줘."
            },
            {
            "role": "user",
            "content": "심심한 사과의 말씀 드립니다."
            },
            {
            "role": "assistant",
            "content": "깊은 사과의 말씀 드립니다."
            },
            {
            "role": "user",
            "content": "심심한 위로의 말씀 드립니다."
            },
            {
            "role": "assistant",
            "content": "따뜻한 위로의 말씀 드립니다."
            },
            {
            "role": "user",
            "content": "금일까지 프로젝트를 끝내 주시겠어요?"
            },
            {
            "role": "assistant",
            "content": "오늘까지 프로젝트를 끝내 주시겠어요?"
            },
            {
            "role": "user",
            "content": "사흘 뒤에 축제가 있다."
            },
            {
            "role": "assistant",
            "content": "3일 뒤에 축제가 있다."
            },
            {
            "role": "user",
            "content": "나흘 전에 전투가 있었다."
            },
            {
            "role": "assistant",
            "content": "4일 전에 전투가 있었다."
            },
            {
            "role": "user",
            "content": "이레 뒤는 내 생일이다."
            },
            {
            "role": "assistant",
            "content": "7일 뒤는 내 생일이다."
            },
            {
            "role": "user",
            "content": "열흘 뒤는 우리 가족이 제사를 하는 날이다."
            },
            {
            "role": "assistant",
            "content": "10일 뒤는 우리 가족이 제사를 하는 날이다."
            },
            {
            "role": "user",
            "content": "여드레 뒤는 규민이의 생일이다."
            },
            {
            "role": "assistant",
            "content": "8일 뒤는 규민이의 생일이다."
            },
            {
            "role": "user",
            "content": "아흐레 뒤는 쇼핑을 하는 날이다."
            },
            {
            "role": "assistant",
            "content": "9일 뒤는 쇼핑을 하는 날이다."
            },
            {
            "role": "user",
            "content": "엿새 뒤는 몇월 몇일일까?"
            },
            {
            "role": "assistant",
            "content": "6일 뒤는 몇월 몇일일까?"
            },
            {
            "role": "user",
            "content": "닷새 전은 무슨 요일일까?"
            },
            {
            "role": "assistant",
            "content": "5일 전은 무슨 요일일까?"
            },
            {
            "role": "user",
            "content": "너 정말 이지적이구나"
            },
            {
            "role": "assistant",
            "content": "너 정말 똑똑하구나"
            },
            {
            "role": "user",
            "content": "항상 무운을 빌게"
            },
            {
            "role": "assistant",
            "content": "항상 행운을 빌게"
            },
            {
            "role": "user",
            "content": "너 고지식하다"
            },
            {
            "role": "assistant",
            "content": "너 융통성이 없다"
            },
            {
            "role": "user",
            "content": "고지식한 사람"
            },
            {
            "role": "assistant",
            "content": "융통성 없는 사람"
            },
            {
            "role": "user",
            "content": "무안하다"
            },
            {
            "role": "assistant",
            "content": "뻘쭘하다"
            },
            {
            "role":"user",
            "content": text
            }
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    return response['choices'][0]['message']['content']

@app.route('/api/ocr', methods=['POST'])
def api_ocr():
    if request.method != "POST":
        return jsonify({"result" : "fail"})

    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "Missing image data"}), 400

    base64_image = data["image"]
    result = process_ocr(base64_image)

    cnt = 0
    answer = ""
    while True:
        try:
            answer += result['words'][cnt]['text'] + " "
            print(result['words'][cnt]['text'], end=" ") 
            cnt += 1
        except:
            break
            
    return {"result": answer}

def find_simi_words(text):
    if request.method != "POST":
        return jsonify({"result" : "fail"})
    verb_list = okt.morphs(text, stem=True)
    verb_list_t = []
    for i in range(len(verb_list)):
        if verb_list[i][-1] == '다':
            verb_list_t.append(verb_list[i])
    noun_list = okt.nouns(text)
    answer = []
    for v in noun_list+verb_list_t:
        datas = {"params": {"dicType": "syn","pageNum": 0,"pageSize": 10,"searchWord": v,"wordGrade": 99, "userid":1}}
        json_data = json.dumps(datas)
        mean = requests.post('https://www.natmal.com/api/dic/Syn/search/searchWordItems', data=json_data, headers={'Content-Type': 'application/json', 'charset': 'UTF-8'})
        try:
            print(())
            print()
            print()
            word_level = (mean.json())['results']['wordInfoItems'][0]['WORD_LEVEL']
            part_speech = (mean.json())['results']['wordInfoItems'][0]['PART_SPEECH']
            print(word_level)
            print(part_speech)
            print()
            print()
            sim_word = gpt_response_sim_word(v)
            print(type(sim_word))
            print(sim_word)
            print([sim_word[sim_word.find('['):-1].split(', ')])
            answer.append({"origin_word":v,"synonym":[sim_word[sim_word.find('['):-1].split(', ')], "mean":(mean.json())["results"]["wordInfoItems"][0]["DEFINITION"], "word_level":word_level, "part_speech":part_speech})
            print({"origin_word":v,"synonym":[gpt_response_sim_word(v).split(', ')], "mean":(mean.json())["results"]["wordInfoItems"][0]["DEFINITION"], "word_level":word_level, "part_speech":part_speech})
            print()
            print()
        except:
            pass
    return answer

@app.route('/api/gpt', methods=['POST'])
def api_gpt():
    if request.method != "POST":
        return jsonify({"result" : "fail"})

    data = request.get_json()

    text = data["text"]
    response = gpt_response(text)
    # requests.post("", find_simi_words(text))
    find_simi_words(text)
    return jsonify({"result": response})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)