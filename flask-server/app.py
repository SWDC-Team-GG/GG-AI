from flask import Flask, request
from konlpy.tag import Okt
import requests
from flask_cors import CORS
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
okt = Okt()

def findWords(word):
    res = requests.post(os.getenv('BASE_URL') + "/searchWordItems", json={
        "params": {
            "dicType": "syn",
            "pageNum": 0,
            "pageSize": 10,
            "searchWord": word,
            "wordGrade": 99
        }})
    res = res.json()
    res = res["results"]["wordInfoItems"]
    res = [
            {
                "wordId": wordInfoItem["WORD_NO"],
                "name": wordInfoItem["WORD_NAME"],
                "meaning": wordInfoItem["DEFINITION"],
                "part": wordInfoItem["PART_SPEECH"]
            }
           for wordInfoItem in res if word == wordInfoItem["WORD_NAME"]
           ]
    return res

def findSimilarWords(wordInfo):
    res = requests.post(os.getenv('BASE_URL') + "/selectedWordItem", json={
        "params": {
            "itemId": wordInfo['wordId'],
            "itemLevel": 4,
            "showType": 1,
            "userId": 1,
            "viewDepth": 1,
            "viewType": "List"
        }})
    res = res.json()
    res = res["synFirstItems"]
    res = [
        {
            "name": wordInfoItem["WORD_NAME"],
            "level": int(wordInfoItem["WORD_LEVEL"])
        }
        for wordInfoItem in res
    ]
    return res

def findCorrectWord(text, wordInfos):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "원래의 문장과 그 문장에서 사용된 단어를 제공받고, 그 단어의 모든 사전적 의미 중 그 문장에서 사용된 의미를 선택해야 한다. 다음과 같은 출력형식을 가져야 한다: index"
            },
            {
            "role": "user",
            "content": "나는 이 입장을 고수하겠다., 고수하다, [차지한 물건이나 형세 따위를 굳게 지키다., 근심과 걱정으로 괴로워하다., 머리를 조아리어 존경의 뜻을 나타내다.]"
            },
            {
            "role": "assistant",
            "content": "0"
            },
            {
            "role": "user",
            "content": f"{text}, {wordInfos[0]['name']}, {[wordInfo['meaning'] for wordInfo in wordInfos]}"
            },
        ],
        temperature=0,
        max_tokens=1024,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0
    )
    return res['choices'][0]['message']['content']

def findNearNum(exList, values):
    res = min(exList, key=lambda x:abs(x['level']-values))
    return res

@app.route('/translate', methods=['GET'])
def translate():
    text = request.args.get('text')
    education = request.args.get('education')
    field = request.args.get('field')
    res = okt.pos(text, stem=True)
    
    #불용어 처리
    res = [word for word in res 
           if word[1] != 'Josa' and len(word[0]) > 1]
    
    #명사 + 하다 => 동사 결합
    for i in range(len(res)):
        if (res[i-1][1] == "Noun" and res[i][0] == "하다"):
            res[i-1] = [res[i-1][0]+"하다", "Verb"]
            res[i] = ""
    res = [word for word in res if word]
    
    #단어 처리
    wordInfos = []
    for item in res:
        words = findWords(item[0])
        if words:
            wordInfos.append(words[int(findCorrectWord(text, words))])
    
    if len(words) == 0:
        return { "translateText": text, "translateWords": None }
    
    #유의어 검색
    similarWord = []
    for wordInfo in wordInfos:
        similarWords = findSimilarWords(wordInfo)
        similarWord.append(findNearNum(similarWords, float(field)*float(education)/10))

    #단어와 유의어 묶기
    translateWords = []
    for index, wordInfo in enumerate(wordInfos):
        translateWords.append(
                                {
                                    "plainWord": wordInfo['name'], 
                                    "translateWord": similarWord[index]['name'],
                                    "translateWordLevel": similarWord[index]['level'],
                                    "meaning": wordInfo['meaning'],
                                    "part": wordInfo['part']
                                }
                            )
    
    translateText = text
    for translateWord in translateWords:
        if translateWord['part'] == "동사":
            translateText = translateText.replace(translateWord['plainWord'][:-1], translateWord['translateWord'][:-1])
        else:
            translateText = translateText.replace(translateWord['plainWord'], translateWord['translateWord'])
        
    
    return {"translateText": translateText, "translateWords": translateWords}
    

if __name__ == "__main__":
    app.run()