# utils-for-images-videos

이미지/비디오 처리용 유틸리티 모음

## depth_to_mask.py

깊이맵 이미지를 이진 마스크(0/255)로 변환한다. 임계값(threshold) 이상이면 255(흰색), 미만이면 0(검정)으로 변환.

### 의존성

```bash
pip install opencv-python numpy
```

### 사용법

#### 단일 이미지

```bash
# 기본 (threshold=128)
python depth_to_mask.py -i depth.png -o mask.png

# threshold 지정
python depth_to_mask.py -i depth.png -o mask.png -t 200

# 반전 모드 (threshold 미만 → 255, 이상 → 0)
python depth_to_mask.py -i depth.png -o mask.png -t 100 --invert
```

#### 폴더 일괄 처리

```bash
# 폴더 내 모든 이미지 변환
python depth_to_mask.py -i ./depth_folder -o ./mask_folder -t 150

# 반전 모드로 폴더 일괄 처리
python depth_to_mask.py -i ./depth_folder -o ./mask_folder -t 100 --invert
```

### 옵션

| 옵션 | 단축 | 설명 | 기본값 |
|------|------|------|--------|
| `--input` | `-i` | 입력 이미지 경로 또는 폴더 경로 | (필수) |
| `--output` | `-o` | 출력 이미지 경로 또는 폴더 경로 | (필수) |
| `--threshold` | `-t` | 이진화 임계값 (0-255) | 128 |
| `--invert` | | 반전 모드 | False |

### 동작 방식

```
일반 모드:       깊이값 >= threshold → 255 (흰색)
                 깊이값 <  threshold → 0   (검정)

반전 모드:       깊이값 <  threshold → 255 (흰색)
(--invert)      깊이값 >= threshold → 0   (검정)
```

### 지원 포맷

입력: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.tif`
출력: 항상 `.png` (무손실)
