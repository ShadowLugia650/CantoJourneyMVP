globals().update(os=__import__("os")) or globals().update(Image=__import__("PIL.Image").Image) or globals().update(path="Assets/img/PChara") or globals().update(scale=222/1080) or [globals().update(im=Image.open(os.path.join(path, f))) or im.resize((round(im.width * scale), round(im.height * scale))).save(os.path.join(path, "-xpt2_".join(f.rsplit("_", 1)))) for f in os.listdir(path) if f.endswith(".png") and f.count("-") == 2]