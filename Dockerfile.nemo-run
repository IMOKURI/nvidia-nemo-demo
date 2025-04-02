FROM nvcr.io/nvidia/nemo:25.02.01

RUN apt-get update && apt-get install -y socat netcat-openbsd && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip --no-cache-dir install nemo_run[skypilot]
RUN curl -L -o /usr/local/bin/kubectl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x /usr/local/bin/kubectl

CMD ["bash"]
