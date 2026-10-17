from pathlib import Path

import shutil

assets_dir = Path(__file__).parent.parent.resolve() / "assets"


def configure_ocr_model():
    assets_ocr_dir = assets_dir / "MaaCommonAssets" / "OCR"
    if not assets_ocr_dir.exists():
        print(f"File Not Found: {assets_ocr_dir}")
        exit(1)

    ocr_dir = assets_dir / "resource" / "model" / "ocr"
    if not ocr_dir.exists():   # copy default OCR model only if dir does not exist
        shutil.copytree(
            assets_dir / "MaaCommonAssets" / "OCR" / "ppocr_v6" / "small",
            ocr_dir,
            dirs_exist_ok=True,
        )
    else:
        print("Found existing OCR directory, skipping default OCR model import.")


def configure_korean_ocr_model():
    # 預設模型讀不出韓文：resource_ko 疊加在 resource 之上，只替換辨識模型（文字框偵測沿用預設）
    ko_dir = assets_dir / "resource_ko" / "model" / "ocr"
    if not (ko_dir / "rec.onnx").exists():
        ko_dir.mkdir(parents=True, exist_ok=True)
        for name in ("rec.onnx", "keys.txt"):
            shutil.copy2(assets_dir / "MaaCommonAssets" / "OCR" / "ppocr_v3" / "ko_kr" / name, ko_dir)
    else:
        print("Found existing Korean OCR model, skipping import.")


if __name__ == "__main__":
    configure_ocr_model()
    configure_korean_ocr_model()

    print("OCR model configured.")
