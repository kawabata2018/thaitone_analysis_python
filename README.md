# thaitone_analysis_python
タイ語声調テスト データ分析用プログラム

## 概要
- Firebase Admin SDKを使ってFirebase Storageの指定ディレクトリ以下のデータを全取得するプログラム

### 参考サイト
https://firebase.google.com/docs/admin/setup?authuser=0  
https://firebase.google.com/docs/auth/admin/manage-users?hl=ja  
https://firebase.google.com/docs/storage/admin/start?hl=ja  
https://cloud.google.com/storage/docs/listing-objects?hl=ja  
https://cloud.google.com/storage/docs/downloading-objects?hl=ja  

## 使い方
### 必要な環境
- python3系

### 手順
- 当レポジトリを適当な場所にクローン
```
git clone https://github.com/kawabata2018/thaitone_analysis_python.git
```
- 必要なパッケージをインストール
```
cd thaitone_analysis
pip install -r requirements.txt
```

- Firebase Admin SDKの秘密鍵をダウンロード（取扱注意！）

- `analysis.py` の73行目 `<yourname>` と `<privatekey.json>` を設定
- `analysis.py` の75行目に、ダウンロードしたいフォルダ名を設定
- Run!
```
python analysis.py
```