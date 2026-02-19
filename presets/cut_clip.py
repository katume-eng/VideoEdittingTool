#!/usr/bin/env python3
"""複数の指定時間から1分のクリップを切り抜くスクリプト"""

import subprocess
import sys

def main():
    # 設定
    base_dir = "/mnt/c/bussiness/song/Tori_1/月影、風の行方"
    input_file = f"{base_dir}/input.mp4"
    output_dir = f"{base_dir}/clips"
    duration = 60  # 秒
    
    # 切り抜きたい開始時間のリスト
    timestamps = [
        "0:00",
        "1:18",
        "1:25",
        "1:40",
        "2:45",
        "2:57",
        "3:49",
        # ここに追加したい時間を書く
    ]
    
    # video-tools コマンドを実行
    cmd = ["video-tools", "cut-fixed", input_file]
    
    # 各タイムスタンプを追加
    for timestamp in timestamps:
        cmd.extend(["--at", timestamp])
    
    cmd.extend(["--duration", str(duration)])

    cmd.extend(["--out-dir", output_dir])
    
    print(f"実行中: {' '.join(cmd)}")
    print(f"{len(timestamps)}個のクリップを作成します...")
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ すべてのクリップ作成完了!")
    except subprocess.CalledProcessError as e:
        print(f"エラー: コマンドが失敗しました", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("エラー: video-tools がインストールされていません", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()