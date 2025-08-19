FROM python:3.10-slim
RUN pip install --no-cache-dir --progress-bar off flask
RUN pip install --no-cache-dir --progress-bar off pymongo
COPY  ./static /home/Desktop/ipa2025-msapp/static/
COPY  ./templates /home/Desktop/ipa2025-msapp/templates/
COPY  app.py /home/Desktop/ipa2025-msapp/
EXPOSE 8080
CMD python /home/Desktop/ipa2025-msapp/app.py

