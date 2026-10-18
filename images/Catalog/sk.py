from pathlib import Path
from PIL import Image
from rembg import remove, new_session

# Папка с исходными картинками
src = Path(r"I:\project\SystemaMSK_10.10.26\v1\systemamsk.ru\images\Catalog\int")
dst = src / "out"
dst.mkdir(exist_ok=True)

# Обрабатываем только файлы, имя которых начинается с этих префиксов
markers = (
    "category-cctv--",
    "category-periphery--",
    "category-workstations--",
)

# False: если файл с таким именем уже лежит в out, он не трогается
OVERWRITE = False

# Если края вырезаются плохо (например, у кабелей), попробуйте другую модель:
# session = new_session("isnet-general-use")
session = new_session()

count = 0
skipped = 0

# glob смотрит только в самой папке int, подпапки (del, out) не затрагиваются
for f in sorted(src.glob("*.webp")):
    if not f.stem.startswith(markers):
        continue

    out_file = dst / f.name
    if out_file.exists() and not OVERWRITE:
        print("пропущено (уже есть в out):", f.name)
        skipped += 1
        continue

    img = Image.open(f).convert("RGB")
    result = remove(img, session=session)
    result.save(out_file, "WEBP", lossless=True)
    count += 1
    print("готово:", f.name)

if count == 0 and skipped == 0:
    print("Файлы не найдены, проверьте путь и названия")
else:
    print(f"Обработано файлов: {count}, пропущено: {skipped}. Результат в папке: {dst}")
