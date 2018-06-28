FROM python
COPY src /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP app.py
EXPOSE 5000/tcp
CMD ["flask", "run", "--host=0.0.0.0"]
