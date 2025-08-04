#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def create_debug_version():
    with open('v2/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # より詳細なデバッグログを追加
    old_error_handling = """                complete: function(results) {
                    if (results.errors.length > 0) {
                        console.error('CSV解析エラー:', results.errors);
                        showUploadStatus('error', '❌ CSVファイルの解析に失敗しました');
                        return;
                    }"""
    
    new_error_handling = """                complete: function(results) {
                    console.log('🔍 PapaParse結果:', results);
                    console.log('📊 データ行数:', results.data.length);
                    console.log('📝 ヘッダー（最初の行）:', results.data[0]);
                    console.log('⚠️ エラー数:', results.errors.length);
                    
                    if (results.errors.length > 0) {
                        console.error('CSV解析エラー詳細:');
                        results.errors.forEach((error, index) => {
                            console.error(`エラー ${index + 1}:`, error);
                            console.error('  タイプ:', error.type);
                            console.error('  コード:', error.code);
                            console.error('  メッセージ:', error.message);
                            console.error('  行番号:', error.row);
                        });
                        showUploadStatus('error', `❌ CSV解析エラー: ${results.errors[0].message}`);
                        return;
                    }"""
    
    content = content.replace(old_error_handling, new_error_handling)
    
    # フィルタリング部分にもデバッグログを追加
    old_filter = """                    // データを変換（新しいCSVフォーマットに対応）
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
    
    new_filter = """                    // データを変換（新しいCSVフォーマットに対応）
                    console.log('🔍 フィールド名確認（最初の行のキー）:', Object.keys(results.data[0] || {}));
                    
                    // フィルタリング前に各行をチェック
                    console.log('📋 最初の3行の内容:');
                    results.data.slice(0, 3).forEach((row, index) => {
                        console.log(`行 ${index + 1}:`, row);
                    });
                    
                    const filteredData = results.data.filter(row => {
                        const hasCustomerName = row['顧客名'] && row['顧客名'].trim() !== '';
                        const hasCheckinTime = row['チェックイン日時'] && row['チェックイン日時'].trim() !== '';
                        const hasStayTime = row['滞在時間'] && row['滞在時間'].trim() !== '';
                        
                        console.log('🔍 行チェック:', {
                            顧客名: row['顧客名'],
                            チェックイン日時: row['チェックイン日時'],
                            滞在時間: row['滞在時間'],
                            有効: hasCustomerName && hasCheckinTime && hasStayTime
                        });
                        
                        return hasCustomerName && hasCheckinTime && hasStayTime;
                    });
                    
                    console.log('✅ フィルタリング後のデータ数:', filteredData.length);
                    
                    EMBEDDED_DATA = filteredData.map(row => ({
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
    
    # ファイル情報もログに追加
    old_file_handling = """        function handleCSVFile(file) {
            showUploadStatus('loading', '📤 CSVファイルを読み込み中...');
            
            Papa.parse(file, {
                header: true,
                encoding: 'UTF-8',"""
    
    new_file_handling = """        function handleCSVFile(file) {
            console.log('📁 アップロードされたファイル情報:');
            console.log('  ファイル名:', file.name);
            console.log('  ファイルサイズ:', file.size, 'bytes');
            console.log('  ファイルタイプ:', file.type);
            console.log('  最終更新:', file.lastModified);
            
            showUploadStatus('loading', '📤 CSVファイルを読み込み中...');
            
            Papa.parse(file, {
                header: true,
                encoding: 'UTF-8',
                skipEmptyLines: true,"""
    
    content = content.replace(old_file_handling, new_file_handling)
    
    # デバッグ版として保存
    with open('v2/index_debug.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ デバッグ版作成完了!")
    print("📁 ファイル: v2/index_debug.html")

if __name__ == "__main__":
    create_debug_version()