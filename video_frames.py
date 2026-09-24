"""Regenerate video posters from selected timestamps."""
from pathlib import Path
import cv2

ASSETS = Path(__file__).parent / 'assets'
for name, seconds in [('cable-tie', 5.0), ('block-sorting', 19.0), ('air-hockey', 15.9), ('long-horizon', 13.0)]:
    cap = cv2.VideoCapture(str(ASSETS / f'{name}.mp4'))
    cap.set(cv2.CAP_PROP_POS_MSEC, seconds * 1000)
    ok, frame = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError(f'Cannot extract {name} at {seconds}s')
    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (1280, round(height * 1280 / width)), interpolation=cv2.INTER_AREA)
    target = ASSETS / f'{name}-poster.jpg'
    if not cv2.imwrite(str(target), frame, [cv2.IMWRITE_JPEG_QUALITY, 88]):
        raise RuntimeError(f'Cannot save {target}')
    print(target.name, target.stat().st_size)
