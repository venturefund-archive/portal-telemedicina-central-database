FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["sphinx-autobuild", ".", "_build/html", "--host", "0.0.0.0", "--port", "8001"]