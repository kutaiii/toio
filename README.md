# Toio

## 環境構築

anacondaを導入しているならカレントディレクトリを移動したのち、以下のコマンドでok  
`conda env create -f environment.yml`

## やること　
- ~~無線によるatomとの通信~~ -> WiFiを介した接続は可能 めっちゃ不安定
- とれるdistanceの値が不安定なため、何かしらの平滑化がいるかも？
- slamをする上での経路計画
- ゴール位置、押す対象物の決定方法
- slamのための荒いピクセルによる環境地図作成
- ~~全体を非同期処理に書きなおし~~   ->　おそらくできた
- いろいろいっぱい

## toioの紙の座標系
![座標](https://github.com/kutaiii/images/blob/main/PXL_20240728_190240290.jpg)