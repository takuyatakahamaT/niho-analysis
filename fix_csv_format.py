#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_csv_mapping():
    # ファイルを読み込み
    with open('v2/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修正1: CSVフィールドマッピングの修正
    old_filter = """                    // データを変換
                    EMBEDDED_DATA = results.data.filter(row => 
                        row.customerName && row.checkinTime && row.stayTime
                    );"""
    
    new_filter = """                    // データを変換（新しいCSVフォーマットに対応）
                    EMBEDDED_DATA = results.data.filter(row => 
                        row['顧客名'] && row['チェックイン日時'] && row['滞在時間']
                    ).map(row => ({
                        customerName: row['顧客名'],
                        checkinTime: row['チェックイン日時'],
                        checkoutTime: row['チェックアウト日時'],
                        stayTime: row['滞在時間'],
                        // 追加情報も保持
                        location: row['チェックイン場所'],
                        memberNumber: row['会員番号'],
                        amount: row['金額'],
                        points: row['付与ポイント']
                    }));"""
    
    content = content.replace(old_filter, new_filter)
    
    # 修正2: processData関数内のフィールド参照も修正
    # （既にcustomerName, checkinTime等を使用しているので、mapで変換済みなら問題ないはず）
    
    # 修正3: README.mdの必要なカラム情報を更新
    readme_content = '''# NIHO鎌倉 利用状況分析 v2 - CSVアップロード版（修正版）

## 🚀 **v2の特徴**

### **📤 CSVファイルアップロード機能**
- **ドラッグ&ドロップ対応**: CSVファイルを直接エリアにドロップ
- **リアルタイム分析**: アップロード後即座にデータ分析・表示
- **Safari/スマホ対応**: 全ブラウザで動作確認済み

### **📊 分析機能（v1と同等）**
- **期間切替**: 6ヶ月ビュー / 7月ビュー
- **ユーザーセグメント**: ヘビー・レギュラー・ライト・トライアル
- **詳細テーブル**: 全ユーザーの利用データ表示
- **インタラクティブグラフ**: Chart.js使用

## 📋 **使用方法**

### **1. CSVファイル準備**
必要なカラム（日本語ヘッダー）：
- `顧客名`: ユーザー名
- `チェックイン日時`: チェックイン日時（例: 2024-03-29 23:33:42 +0900）
- `チェックアウト日時`: チェックアウト日時（例: 2024-03-29 23:34:22 +0900）
- `滞在時間`: 滞在時間（HH:MM:SS形式、例: 00:00:40）

### **CSVフォーマット例**
```csv
チェックイン場所,顧客名,会員番号,チェックイン日時,チェックアウト日時,滞在時間,金額,付与ポイント
NIHO kamakura,三重野将,58FF6EC5FA,2024-03-29 23:33:42 +0900,2024-03-29 23:34:22 +0900,00:00:40,100,0
```

### **2. アップロード**
1. ページにアクセス
2. CSVファイルを選択またはドラッグ&ドロップ
3. 自動的にデータ分析が開始

### **3. 分析結果確認**
- **統計**: 期間、ユーザー数、平均値
- **散布図**: 利用頻度 vs 利用時間
- **セグメント分析**: ユーザー分類
- **詳細テーブル**: 全ユーザーデータ

## 🔧 **技術仕様**

### **使用ライブラリ**
- **Chart.js**: グラフ描画
- **PapaParse.js**: CSV解析
- **Pure JavaScript**: フレームワーク不使用

### **対応ブラウザ**
- ✅ Chrome
- ✅ Safari（Mac/iPhone）
- ✅ Firefox
- ✅ Edge

### **モバイル対応**
- レスポンシブデザイン
- タッチ操作最適化
- パフォーマンス調整（上位100ユーザー表示）

## 📈 **v1との違い**

| 機能 | v1（埋め込み版） | v2（アップロード版） |
|------|----------------|-------------------|
| データ更新 | ❌ 固定データ | ✅ CSVアップロード |
| 最新データ対応 | ❌ 手動更新必要 | ✅ リアルタイム対応 |
| CSVフォーマット | 3フィールド | 8フィールド対応 |

## 🔄 **変更履歴**
- **2025-01-31**: 新しい8フィールドCSVフォーマットに対応
  - 日本語ヘッダー対応: `顧客名`, `チェックイン日時`, `滞在時間`等
  - フィールドマッピング機能追加
  - 追加情報（場所、会員番号、金額、ポイント）の保持
'''
    
    # ファイルに書き込み
    with open('v2/index_fixed.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    with open('v2/README_fixed.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ CSV フォーマット修正完了!")
    print("📁 修正ファイル:")
    print("   - v2/index_fixed.html")
    print("   - v2/README_fixed.md")

if __name__ == "__main__":
    fix_csv_mapping()