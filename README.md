
# 現役ドラフト制度及び改善案の設計

現役ドラフト制度の現行ルールと改善案をシミュレーションするためのスクリプトを含んでいます。現行ルールは`scripts/current_rule.py`に記述されており、改善案は`scripts/enhanced_rule.py`に記述されています。実際のデータや掛け合わせる数値などは`config`に記述されています。

## 構成

- `scripts/current_rule.py`: 現行の現役ドラフト制度に基づいたシミュレーションスクリプト。
- `scripts/enhanced_rule.py`: 改善案に基づいたシミュレーションスクリプト。
- `config/`: 実際のデータやシミュレーションに必要な設定を含むフォルダ。
- `web/index.html`: シミュレーションの実行結果を表示するためのWebページ。（ローカルでサーバーを立ち上げないと機能しません。5. を参照）

## 使用方法

### 1. リポジトリのクローン

まず、リポジトリをローカル環境にクローンする。

```bash
git init
git clone https://github.com/JunkiUchimi/draft_system.git
cd draft_system
```

### 2. 仮想環境のセットアップ

Pythonの仮想環境をセットアップし、必要なパッケージをインストールします。

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. シミュレーションの実行

#### 現行ルールに基づくシミュレーション

```bash
python scripts/current_rule.py
```

#### 改善案に基づくシミュレーション

```bash
python scripts/enhanced_rule.py
```

### 4. 設定ファイルの編集

`config`フォルダ内の設定ファイルを編集して、シミュレーションに使用するデータやパラメータを調整します。

### 5. 結果の表示

シミュレーション結果は`web/index.html`で表示されます。結果を表示するには、ローカルサーバーを起動し、ブラウザで`index.html`を開きます。

```bash
cd web
python -m http.server
```

ブラウザで `http://localhost:8000` を開いて結果を確認します。

## プロジェクトの目的

現行の現役ドラフト制度をシミュレーションし、その結果を分析することで改善案を提案する。改善案に基づくシミュレーションを実施することで、より公平かつ効率的なドラフト制度の設計を目指すこと。

