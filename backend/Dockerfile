# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN ngrok config add-authtoken 2irl2dM8GAcEDEdJPHHDZ5KGSxz_7LfzNg1U2R3yzzjkEWmJo

# 
COPY ./app /code/app

# 
# CMD ["fastapi", "run", "app/main.py", "--port", "80"]
CMD ["python3", "-u", "app/main.py"]
