# Daily Tuja - Vertiv 주식 조회

Vertiv Holdings(VRT) 주식 시세를 Yahoo Finance에서 조회하는 프로그램입니다.

## 기능

- Yahoo Finance에서 Vertiv(VRT) 실시간 주가 조회
- 현재가, 등락폭, 거래량 등 주요 정보 터미널 출력

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

### 실행

```bash
cd src
python main.py
```

### 테스트 실행 (더미 데이터 사용)

```bash
cd src
python main.py --test
```

## 프로젝트 구조

```
daily_tuja/
├── src/
│   ├── main.py           # 메인 스크립트
│   └── stock_fetcher.py  # 주식 데이터 조회 모듈
├── .gitignore
├── requirements.txt
└── README.md
```

## 출력 예시

```
📈 Vertiv Holdings Co (VRT) 시세
----------------------------------------
  현재가:      $95.50
  전일 종가:   $92.30
  등락:        +$3.20 (+3.47%)
  고가 / 저가: $96.20 / $91.80
  거래량:      5,234,567
  시가총액:    $35.00B
----------------------------------------
  📊 데이터 출처: Yahoo Finance
```

## 주의사항

- 미국 증시 휴장일에는 데이터가 업데이트되지 않습니다
- Yahoo Finance API는 약간의 지연이 있을 수 있습니다
