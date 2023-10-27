from fastapi import FastAPI
from pydantic import BaseModel
from summa import summarizer

def summarize(text):
    """
    주어진 긴 텍스트를 요약하는 함수
    :param long_text: 긴 텍스트
    :return: 요약 텍스트
    """
    summary = summarizer.summarize(text, words=30)  # 요약을 위한 단어 수 조절
    return summary

# 긴 텍스트 예제
text = """
김주현 금융위원장이 27일 국회 정무위원회 국정감사에서 공매도 제도를 원점에서 재점검하겠다고 밝힌 것은 개인투자자에게 불리한 ‘기울어진 운동장’을 바로잡겠다는 강력한 의지의 표현으로 읽힌다. 자본시장에서 불공정한 시장 관행을 바로잡겠다는 정부의 계획의 일환이다.

김 위원장의 이날 발언은 2주전 국정감사에서와는 전혀 다른 모습이다. 일부 의원들이 제기하던 강한 규제에 대해서 현실상 불가능하다고 반박하던 김 위원장이 공매도 전면 금지를 언급한 윤창현 국민의힘에 ‘제도 개선’으로 화답했기 때문이다.

이는 불법 공매도 문제에 적극적으로 대응할 필요가 커졌기 때문이다. 외국계IB들의 무차입 공매도 등 불법 공매도가 한국 증시를 교란하는 상황을 해결해야 한다는 문제의식이 금융당국 사이에서 공유되고 있는 것이다. 실제로 금융당국은 이런 문제 사례를 다수 발견하고 조사 중인 것으로 알려졌다.

금융감독원은 지난 12일 예정에 없던 브리핑을 열고 글로벌 투자은행(IB)들이 장기간 고의적으로 불법 공매도를 저질러온 사실을 적발했다고 밝혔다.

이들은 차입한 주식수 보다 부풀린 양을 공매도했고, 이같은 불법행위는 최소 수 개월간 계속됐다. 현재 국내 자본시장에서 공매도를 하려면 미리 주식을 빌려놓고 빌린 수 만큼만 공매도를 해야 하지만, 이들은 앞으로 빌릴 수 있을 것 같은 주식 수 만큼을 빌리지도 않은 상태에서 공매도 했다. 그간 투자자들 사이에서 회자되던 무차입 공매도가 횡행한다는 소문이 사실로 드러난 순간이다.

불법 공매도로 인한 시장교란 기능이 단순 제도 개선으로 해결이 쉽지 않다고 판단될 경우 공매도 금지 같은 강력한 조치도 나올 수 있다.

다만 반시장적 규제란 비판이 나올 수 있고 일부 외국인 자금 유출이 일어날 수 있다는 문제도 있다. 거래소 관계자는 “우리 증시가 강한 규제에도 불구하고 외국인 투자자들에게 매력적인 시장이냐의 문제다”라며 “외국인이나 기관 입장에서는 헤지 수단이 필요하다는 점도 감안해야 한다”고 말했다.
"""

summary = summarize(text)
print(summary)

# 🔉 fastapi 서버 
app = FastAPI()

class InputText(BaseModel):
    text:str

@app.post("/summarize")
def post_summarize(input_text:InputText):
    summary = summarize(input_text.text)
    return {"summary":summary}