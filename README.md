# VOICEVOX Engine Wrapper for Python 3

voicevox_engineのHTTPサーバーにリクエストを送るPython3用のラッパーです。

## セットアップ
### voicevox_engineのセットアップ
[VOICEVOX/voicevox_engine](https://github.com/VOICEVOX/voicevox_engine)をクローンして、好きなやり方でセットアップしてください。

### 必要なライブラリをインストール
生成した音声をその場で再生する機能を使う場合、pygamesをインストールします。
```bash
python3 -m pip install pygames
```
---

## プログラムの例
```python3
import voicevox
client = voicevox.Client()
request = client.request("あいうえお", 3)
query = request.request_query()
voice = query.request_voice()
voice.play()
```

---


## クラス・関数
### クラス: `Client(server: Union[str, Server] = "localhost:50021") -> None`
サーバーのip:portを指定するクラス。  
初期化時の返り値は無し。
#### 関数: `Client.request(text: str, speaker: int = 3) -> Request`
喋らせる文字列と喋らせるキャラクターを指定する関数。  
返り値は初期化された`Request`クラス。

### クラス: `Request(client: Client, text: str, speaker: int) -> None`
サーバーに各種リクエストをするクラス。  
初期化時の返り値は無し。
#### 関数: `Request.request_query(None) -> Query`
サーバーからクエリ用jsonを取得する。  
返り値は初期化された`Query`クラス。
#### 関数: `Request.request_voice(query: Query) -> Voice`
サーバーにQueryクラスのjsonを送信し、音声を取得する。  
返り値は初期化された`Voice`クラス。

### クラス: `Query(query: dict, request: Request, client: Client) -> None`
クエリのクラス。  
初期化時の返り値はなし。また、初期化処理以外の関数なし。

### クラス: `Voice(data: bytes, query: Query) -> None`
音声データのクラス。初期化時の返り値はなし。
#### 関数: `Voice.save(output: str) -> None`
音声データを`output`に保存する。  
返り値はなし。
#### 関数: `Voice.play() -> None`
音声データを一時ファイルに保存し、再生する。  
返り値はなし。

---

## 実行
1. voicevox_engineを起動する
2. プログラムを実行する