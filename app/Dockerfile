# dockerfile, Image, Container

FROM python:3.11.4

#add files
ADD requirements.txt .
ADD main.py .
ADD fix_compiled_path.py .
ADD houdini_setup_linux.py .
ADD houdini_setup_mac.py .
ADD houdini_setup_shared.py .
ADD houdini_setup_windows.py .
ADD pysoma_lib.py .
ADD main_config.yml .
ADD project_template_master.yml .


#install like from terminal  dependencies
RUN python3 -m venv /opt/venv
# RUN ls ./venv/


COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

WORKDIR /app
COPY . /app

VOLUME /host_files

COPY main.py .



#run as if in terminal
CMD . /opt/venv/bin/activate && exec python main.py
# CMD ["python", "./main.py"]

