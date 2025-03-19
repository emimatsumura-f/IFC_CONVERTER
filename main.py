import ifcopenshell

def extract_profile_information(element):
    """
    IFCの要素からプロファイル情報を抽出する
    
    Args:
        element: IFC要素（IFCBEAMまたはIFCCOLUMN）
        
    Returns:
        str: プロファイル名称（Description属性の値）
    """
    try:
        return element.Description
    except:
        return None

def main():
    # IFCファイルを読み込む
    file_path = "20241102.ifc"    # ファイルパスを修正
    
    try:
        ifc_file = ifcopenshell.open(file_path)
        
        # BeamとColumnの要素を取得
        beams = ifc_file.by_type('IfcBeam')
        columns = ifc_file.by_type('IfcColumn')
        
        print("=== IFCBEAMとIFCCOLUMNの情報 ===\n")
        
        # Beamの情報を出力
        print("Beams:")
        for beam in beams:
            profile = extract_profile_information(beam)
            if profile:
                print(f"{profile}")
        
        # Columnの情報を出力
        print("\nColumns:")
        for column in columns:
            profile = extract_profile_information(column)
            if profile:
                print(f"{profile}")
    
    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()