import os

template = '''<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Места погружений в Текирова в районе трех островов</title>
    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
    <style>
        .image-container {{
            height: 30vh;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .image-container img {{
            max-height: 100%;
            width: auto;
            max-width: 100%;
        }}
    </style>
</head>
<body class="bg-dark text-light">
    <header class="bg-black text-white py-4 mb-4">
        <div class="container text-center">
            <h1 class="display-4"> Места погружений в Текирова в районе трех островов</h1>
            <h3 class="lead"> Оригинальные имиджи взяты с сайта <a href=\"http://ru.tekirovadiving.com/\">Дайвинг-центра Текирова (Турция)</a></h3>
        </div>
    </header>
    <div class="container">
        <div class="row row-cols-1 row-cols-md-3 g-4">
            {images}
        </div>
    </div>
    <footer class="bg-black text-white py-3 mt-5">
        <div class="container text-center">
            <p class="mb-0">Все права на изображения принадлежат <a  href="http://ru.tekirovadiving.com/">Tekirova Diving Center.</a></p>
            <p class="mb-0">© 2025 Места погружений в Текирова в районе трех островов. Все права защищены.</p>
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''


def generate_gallery(image_folder, output_file):
    images_html = ""
    images = [img for img in os.listdir(image_folder) if img.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]

    for index, image in enumerate(images):
        images_html += f'''
        <div class="col">
            <div class="card bg-secondary h-100">
                <div class="image-container">
                    <a href="http://ru.tekirovadiving.com/mesta-dlya-pogrujeniya" class="text-center">
                        <img src="{image_folder}/{image}" class="rounded" alt="Image">
                    </a>
                </div>
            </div>
        </div>'''

    html_content = template.format(images=images_html)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Gallery saved to {output_file}")


# Пример использования
generate_gallery("downloaded_images", "index.html")