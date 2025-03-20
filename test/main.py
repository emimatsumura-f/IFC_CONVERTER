# IFCファイルを処理するためのライブラリをインポート
import ifcopenshell

def extract_profile_information(element):
    """
    IFCの要素からプロファイル情報を抽出する関数
    
    Args:
        element: IFC要素（IFCBEAMまたはIFCCOLUMN）
                建築モデル内の梁や柱の要素を表すオブジェクト
        
    Returns:
        str: プロファイル名称（Description属性の値）
             属性が存在しない場合はNoneを返す
    """
    try:
        # Description属性からプロファイル情報を取得
        return element.Description
    except:
        # 属性が存在しない場合はNoneを返す
        return None

def main():
    # 処理対象のIFCファイルパスを指定
    file_path = "20241102.ifc"  
    
    try:
        # IFCファイルを読み込んでパース
        ifc_file = ifcopenshell.open(file_path)
        
        # IFCファイルから梁(Beam)と柱(Column)の要素を抽出
        # by_type()メソッドは指定したタイプの要素をすべて取得
        beams = ifc_file.by_type('IfcBeam')    # すべての梁要素
        columns = ifc_file.by_type('IfcColumn') # すべての柱要素
        
        print("=== IFCBEAMとIFCCOLUMNの情報 ===\n")
        
        # 梁(Beam)の情報を出力
        print("Beams:")
        for beam in beams:
            profile = extract_profile_information(beam)
            if profile:
                print(f"{profile}")
        
        # 柱(Column)の情報を出力
        print("\nColumns:")
        for column in columns:
            profile = extract_profile_information(column)
            if profile:
                print(f"{profile}")
    
    except FileNotFoundError:
        # 指定されたIFCファイルが存在しない場合のエラーハンドリング
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        # その他の予期せぬエラーのハンドリング
        print(f"エラーが発生しました: {str(e)}")
    
# スクリプトが直接実行された場合のみmain()を実行
if __name__ == "__main__":
    main()