# [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

1. インストール＆初期化

```bash
$ createdb mhotta       # データベース作成
$ . /path/to/venv/bin/activate
$ pip install alembic   # SQLAlchemy も同時に入る
$ pip install psycopg2  # PostgreSQL サポート
$ mkdir alembic-tutorial && cd alembic-tutorial
$ alembic init alembic
$ vi alembic.ini        # sqlalchemy.url に接続文字列 'postgresql://mhotta:@localhost/mhotta' をセット
```

2. マイグレーションファイルの作成

ファイル名は自動生成されるので、適宜読み替えること。

```bash
$ alembic revision -m "create account table"
Generating /home/mhotta/alembic-tutorial/alembic/versions/2b56acf7a7fe_create_account_table.py ...  done
$ vi alembic/versions/2b56acf7a7fe_create_account_table.py
# def upgrade(): 配下を以下で上書き
```

```python
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
```

3. マイグレーションの実行

```bash
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 2b56acf7a7fe, create account table
```

引数 head は『最新バージョン』の別名である。

4. 作成されたテーブルの確認

```bash
$ echo "\d account" | psql mhotta
                                       テーブル"public.account"
     列      |         タイプ         | 照合順序 | Null 値を許容 |             デフォルト
-------------+------------------------+----------+---------------+-------------------------------------
 id          | integer                |          | not null      | nextval('account_id_seq'::regclass)
 name        | character varying(50)  |          | not null      |
 description | character varying(200) |          |               |
インデックス:
    "account_pkey" PRIMARY KEY, btree (id)
```

5. テーブルに last_transaction_date カラムを追加する

```bash
$ alembic revision -m "add a column"
Generating /home/mhotta/alembic-tutorial/alembic/versions/84cdd9bb8fce_add_a_column.py ...  done
$ vi alembic/versions/84cdd9bb8fce_add_a_column.py 
# def upgrade(): 配下を以下で上書き
```

```python
def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')
```

```bash
$ alembic upgrade head
```

6. 部分的なリビジョンID

リビジョン番号は、先頭の数文字を指定すればよい（git のブランチ名と同じ）。この番号がバージョンを一意に識別する限り、バージョン番号を受け付けるあらゆる場所のコマンドで使用することができる。

```bash
$ alembic upgrade 84c
```

上記では、リビジョン 84cdd9bb8fce を指すために 84c を使用した。 Alembic は、その接頭辞で始まるバージョンが複数ある場合、停止して通知する。

また、upgrade +2 や downgrade -1 のように、 相対的なバージョン指定も可能。

7. 現状の確認

マイグレーションの適用状況を確認する。

```bash
$ alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
84cdd9bb8fce (head)
```

適用履歴を確認する。

```bash
$ alembic history --verbose
Rev: 84cdd9bb8fce (head)
Parent: 2b56acf7a7fe
Path: /home/mhotta/alembic-tutorial/alembic/versions/84cdd9bb8fce_add_a_column.py

    add a column
    
    Revision ID: 84cdd9bb8fce
    Revises: 2b56acf7a7fe
    Create Date: 2024-03-07 16:37:28.107154

Rev: 2b56acf7a7fe
Parent: <base>
Path: /home/mhotta/alembic-tutorial/alembic/versions/2b56acf7a7fe_create_account_table.py

    create account table
    
    Revision ID: 2b56acf7a7fe
    Revises: 
    Create Date: 2024-03-07 16:08:56.566597
```

その他、heads や branches 等のサブコマンドがある。 --verbose オプションはこれらでも指定可能。

7. ダウングレード

変更を元に戻す。『最初』を表すブランチ名は base である。

```bash
$ alembic downgrade base
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 84cdd9bb8fce -> 2b56acf7a7fe, add a column
INFO  [alembic.runtime.migration] Running downgrade 2b56acf7a7fe -> , create account table
$ echo "\d account" | psql mhotta
"account"という名前のリレーションは見つかりませんでした。
```
