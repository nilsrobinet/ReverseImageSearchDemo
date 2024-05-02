FROM python:3.11.6

WORKDIR /app/

#Set up requirements
COPY ./requirements.txt /app/requirements.txt
COPY ./requirements_torch.txt /app/requirements_torch.txt

RUN pip install -Ur ./requirements.txt
RUN pip install -Ur ./requirements_torch.txt

# Copy application into image
COPY . /app/

# Open CherryPy server port
EXPOSE 8081
EXPOSE 19530

CMD ["python3", "Server.py"]