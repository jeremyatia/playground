FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)

RUN yum update -y && yum install -y sudo
RUN yum upgrade -y

# Install curl
RUN yum install -y curl

# Install ca-certificates and gnupg
RUN yum install -y ca-certificates gnupg

# Install Node.js (NodeSource repository for CentOS)
RUN curl -sL https://rpm.nodesource.com/setup_18.x | sudo bash -
RUN yum install -y nodejs


# Install GTK and other dependencies
RUN yum install -y gtk2
RUN yum install -y epel-release
RUN yum install -y gbm
RUN yum install -y nss nss-tools xorg-x11-server-Xvfb gtk3

# To allow MP3 conversion, install ffmpeg (from the RPM Fusion repository)
RUN yum install -y epel-release
RUN rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
RUN rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
RUN yum install -y ffmpeg


# Set environment variable
ENV LC_ALL=en_US.UTF-8


CMD [ "lambda_function.handler" ]










