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

# Implementation details : 
Code implemented using Python 3.9 + Fast API framework. 
Run the server with: 
```bash
        uvicorn main:app --reload
```
For more infomraion visit: https://fastapi.tiangolo.com/
Assumptions: 
- In the system exist users and each user has id.
- For simpicity system recieve only images in following formats: jpg, jpeg, png.
- Each image recieve id based on <userId_UUID>. UUID is 128-bit number used to identify information in computer systems.
UUId has a very low probability of getting collisions. For more information: https://en.wikipedia.org/wiki/Universally_unique_identifier
- Currenly system work only with 256x256 sizes. But there exist a posibility to change provided sizes. Such that if in the future 
you will need to handle additional size like 64x64 the main logic that calculate and save tiles handle this case.
- The system performs a check to ensure that the size of the file does not exceed 1 gigabyte (1GB)


The system incorporates a basic cropping algorithm that is designed to crop images to a fixed requested size of 256x256 pixels.
Improvements: If user add the same picture twice but with different tiles it should save only new tiles, without original image. 
How can we do it: We can calculate hash for current image using SHA-1 or MD-5 and save it next to image_id/DB. The same images has the same hash. 

/get_tiled_images endpoint: retrurned as zip file. 

Security: 
- Access control: users.
- User can't upload large files
- Basic CORS implemented
- Input Validation
- only valid types accepted
- logs were added to check upload activity.  In the future worth to scan logs in real time.

Improvements: 
- Rate Limiter to prevent DOS atacks/restrict number of tryes per unit of time.
- Scan for malicious content

Tests:
- Implemented partuculary 