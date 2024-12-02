import rawpy 
import cv2 
import os 
from PIL import Image 
from pillow_lut import load_cube_file 
import numpy as np 
import sys 
 
def convert_raw_to_tif_with_lut(raw_filename, lut_path): 
    # RAWファイルを読み込む 
    with rawpy.imread(raw_filename) as raw: 
        # RAWデータを画像に変換 
        processed_image = raw.postprocess( 
            #no_auto_bright=True, 
            bright=0.90, 
            demosaic_algorithm=rawpy.DemosaicAlgorithm.DCB, 
            noise_thr=20, 
            median_filter_passes=0, 
            fbdd_noise_reduction=rawpy.FBDDNoiseReductionMode.Full, 
            use_camera_wb=True 
        ) 
 
    # LUTを適用する 
    lut = load_cube_file(lut_path) 
    im = Image.fromarray(processed_image)  # Numpy arrayをPillowのImageに変換 
    im_with_lut = im.filter(lut)  # LUTを適用 
 
    # 入力ファイルのディレクトリを取得 
    input_dir = os.path.dirname(raw_filename) 
 
    # 出力ファイル名を設定（元の画像と同じ場所に保存） 
    output_filename = os.path.join(input_dir, os.path.basename(raw_filename)
        .replace('.NEF', '-lut.jpg')
        .replace('.nef', '-lut.jpg')
        .replace('.DNG', '-lut.jpg')
        .replace('.dng', '-lut.jpg')
        .replace('.CR3', '-lut.jpg')
        .replace('.cr3', '-lut.jpg')
        .replace('.RAF', '-lut.jpg')
        .replace('.raf', '-lut.jpg')
        .replace('.ARW', '-lut.jpg')
        .replace('.arw', '-lut.jpg'))
 
    # 結果をJPEG形式で保存 
    im_with_lut.save(output_filename, format="JPEG", quality=100) 
    print(f"Saved with LUT applied: {output_filename}") 
 
if __name__ == "__main__": 
    # コマンドライン引数（ファイルパス）を取得 
    raw_filename = sys.argv[1] 
    lut_file = "mk_neko_4.cube"  # 使用するLUTファイルのパス 
 
    # 処理対象の拡張子リスト 
    valid_extensions = {'.nef', '.NEF', '.dng', '.DNG', '.cr3', '.CR3', '.raf', '.RAF', '.arw', '.ARW'}

 
    # 拡張子チェック（小文字で比較） 
    if os.path.splitext(raw_filename.lower())[1] in valid_extensions: 
        # NEFまたはDNGを読み込んでLUTを適用し、TIFFで保存 
        convert_raw_to_tif_with_lut(raw_filename, lut_file) 
    else: 
        print(f"Unsupported file extension: {raw_filename}") 
