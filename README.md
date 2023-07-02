# doi2notion-py

## Overview
DOIをもとに検索した文献のメタデータをNotionデータベースに追加するPythonスクリプト

- DOIからメタデータを取得（[Crossref API]("https://github.com/fabiobatalha/crossrefapi")を使用）
- 文献データを加工してNotionデータベースに保存（Notionインテグレーション）
- 追加対象：
  - メタデータ：DOI, Title, Author(s), Journal, Year(issued), Month(issued)
  - 被引用件数
 
### Limitations
- DOIが付与されていない文献（一部会議など）
- arXivなどDOIが付与されていてもCrossrefに非対応の文献

## Getting started

### Requirements
- Notion Integration (Secret Key)
- Python (3.9 or higher required)
- Python Libraries: python-dotenv, crossrefapi, tqdm

### Preparation

#### Step1.
Notionの [My Integration]("https://www.notion.so/my-integrations") からシークレットキーを発行します．
1. 「+ 新しいインテグレーション」
1. 関連ワークスペースを選択 & インテグレーション名（任意）を入力 → 「送信」
1. 「内部インテグレーションシークレット」をメモ
1. 「機能」タブを開き，「コンテンツ機能」のすべての項目にチェックを付ける → 「変更を保存」

#### Step2.
リポジトリをクローンします．
```bash
$ git clone git@github.com:KaiSugahara/doi2notion-py.git
```
OR
```bash
$ git clone https://github.com/KaiSugahara/doi2notion-py.git
```

#### Step3.
次のカラムを持つNotionデータベースを作成します．
| Field Name | Field Type |
| :---: | :---: |
| DOI | `title` |
| Title | `rich_text` |
| Authors | `multi_select` |
| Journal | `rich_text` |
| Year | `number` |
| Month | `number` |
| Abstract | `rich_text` |
| Citations | `number` |

続いて，`共有` > `リンクをコピー` からデータベースIDを抽出しメモします．
```
https://www.notion.so/ksugahara/xxxxxxxxxxxxxxxxxxxxxxxxxxx?v=84659eea0c59489f83adb3be8fbd5023&pvs=4
```
の「xxxxxxxxxxxxxxxxxxxxxxxxxxx」部分がデータベースIDです．


#### Step4.

作成したインテグレーションに作成したデータベースへのアクセスを許可します．
1. 対象のデータベースを開く
1. 右上の $\cdots$ の `コネクトの追加`
1. 作成したインテグレーション名を選択
1. はい

#### Step5.
環境変数の設定ファイルを作成します．
```bash
$ cd doi2notion-py
$ cp .env.example .env
$ vi .env
```

インテグレーションのシークレットキーとデータベースIDを入力し，保存します．
```
NOTION_SECRET=your_secret_key
NOTION_DATABASE_ID=your_database_id
```

### Adding New Paper to Notion Database

#### Step1.

追加したい文献のDOIを用意します．
```
10.1016/j.patcog.2023.109657
```
#### Step2.

DOIを渡して，`add.py`を実行します．

```bash
$ python3 add.py 10.1016/j.patcog.2023.109657
```

#### Memo.
DOIを複数渡すこともできます．
```bash
$ python3 add.py 10.1016/j.patcog.2023.109657 10.1145/956750.956764 10.1007/s10115-015-0823-x
```

### Updating Papers in Notion Database

追加済みの文献メタデータを最新に一括更新できます．<br>
（メタデータは滅多に変わることはありませんが，被引用件数の更新に便利です）
```bash
$ python3 update.py
```
