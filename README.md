# ImageTilerApi 💡
Backend service that allows users to upload and tile panoramic images. The service should take a large
panoramic image and divide it into smaller tiles, which can be displayed as a seamless mosaic
on a web page.
System Requirements:
1. Implement an API endpoint for uploading a panoramic image file.
2. Write a function or method that takes the uploaded image and divides it into smaller
tiles. Each tile should have a fixed size (e.g., 256x256 pixels).
3. The tiled images should be stored and associated with the original panoramic image.
4. Implement an API endpoint that retrieves the tiled images for a panoramic image. The
endpoint should return the tiled images as a response, which can be used to display the
panoramic mosaic on a web page.
5. The API should handle errors gracefully and provide appropriate error responses.

Evaluation Criteria:
1. Code organization and readability.
2. Efficient and scalable tile generation algorithm.
3. API design and implementation.
4. Error handling and response consistency.
5. Attention to security and data integrity.

## run project in virtual environment 🚀

- Create virtual env:

```bash
        python -m virtualenv <folder_name>
```

- Create virtual environment version depend:

```bash
        virtualenv <folder_name> --python=python3.9
```

- activate

```bash
  .\<folder_name>\Scripts\activate.bat
```

- ctrl + shift + p: Python: Select interpreter
  should include Python interpreter related to your environment
- refresh terminal
- install requirements:

```bash
        pip install -r requirements.txt
```

- run server: check that you run Fast API


- deactivate:

```bash
        deactivate
```

# Requirements :construction:
Python 3.9+

# Design :zap:
```bash
ImageTilerApi/
|-- app/
| |-- data/
| |-- logs/
| |-- tests/
| |-- main.py
| |-- scyhemas.py
| |-- image.py
| |-- data_loader.py
|-- requirements.txt
|-- README.md
```

# Integrations :pushpin:
- [ ] Slack
- [x] Logs
- [ ] Mail