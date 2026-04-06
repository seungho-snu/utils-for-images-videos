"""
depth_to_mask.py
깊이맵 이미지를 이진 마스크로 변환한다.
임계값(threshold) 이상이면 255(흰색), 미만이면 0(검정)으로 변환.
"""

import argparse
import os
import sys
import cv2
import numpy as np

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}


def depth_to_mask(image_path: str, output_path: str, threshold: int, invert: bool = False):
    """단일 깊이맵 이미지를 이진 마스크로 변환하여 저장한다."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"[ERROR] 이미지를 읽을 수 없음: {image_path}")
        return False

    if invert:
        # threshold 미만이면 255, 이상이면 0 (가까운 물체를 마스킹)
        _, mask = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
    else:
        # threshold 이상이면 255, 미만이면 0 (먼 물체를 마스킹)
        _, mask = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    cv2.imwrite(output_path, mask)
    print(f"[OK] {image_path} → {output_path}  (threshold={threshold}, invert={invert})")
    return True


def process_folder(input_dir: str, output_dir: str, threshold: int, invert: bool = False):
    """폴더 내 모든 이미지에 대해 이진 마스크 변환을 수행한다."""
    os.makedirs(output_dir, exist_ok=True)

    files = sorted([
        f for f in os.listdir(input_dir)
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ])

    if not files:
        print(f"[ERROR] 지원되는 이미지가 없음: {input_dir}")
        return

    print(f"총 {len(files)}개 이미지 처리 시작...")
    success = 0
    for fname in files:
        input_path = os.path.join(input_dir, fname)
        # 출력 파일은 항상 PNG로 저장 (무손실)
        output_name = os.path.splitext(fname)[0] + ".png"
        output_path = os.path.join(output_dir, output_name)
        if depth_to_mask(input_path, output_path, threshold, invert):
            success += 1

    print(f"\n완료: {success}/{len(files)}개 변환됨 → {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="깊이맵 이미지를 이진 마스크(0/255)로 변환한다."
    )
    parser.add_argument("--input", "-i", required=True,
                        help="입력 이미지 경로 또는 폴더 경로")
    parser.add_argument("--output", "-o", required=True,
                        help="출력 이미지 경로 또는 폴더 경로")
    parser.add_argument("--threshold", "-t", type=int, default=128,
                        help="이진화 임계값 (0-255, 기본값: 128)")
    parser.add_argument("--invert", action="store_true",
                        help="반전 모드: threshold 미만이면 255, 이상이면 0")

    args = parser.parse_args()

    if not 0 <= args.threshold <= 255:
        print(f"[ERROR] threshold는 0~255 사이여야 합니다: {args.threshold}")
        sys.exit(1)

    if os.path.isdir(args.input):
        process_folder(args.input, args.output, args.threshold, args.invert)
    elif os.path.isfile(args.input):
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        depth_to_mask(args.input, args.output, args.threshold, args.invert)
    else:
        print(f"[ERROR] 입력 경로를 찾을 수 없음: {args.input}")
        sys.exit(1)


if __name__ == "__main__":
    main()
