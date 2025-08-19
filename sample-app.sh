#!/bin/bash

mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python:3.10-slim" >> tempdir/Dockerfile
echo "RUN pip install --no-cache-dir --progress-bar off flask" >> tempdir/Dockerfile
echo "RUN pip install --no-cache-dir --progress-bar off pymongo" >> tempdir/Dockerfile
echo "COPY  ./static /home/Desktop/ipa2025-msapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/Desktop/ipa2025-msapp/templates/" >> tempdir/Dockerfile
echo "COPY  app.py /home/Desktop/ipa2025-msapp/" >> tempdir/Dockerfile
echo "EXPOSE 8080" >> tempdir/Dockerfile
echo "CMD python /home/Desktop/ipa2025-msapp/app.py" >> tempdir/Dockerfile

cd tempdir
docker build -t web .
docker run -t -d -p 8080:8080 --name web web
docker ps -a 
