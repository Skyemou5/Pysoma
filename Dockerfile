# dockerfile, Image, Container

FROM python:3.11.4

#add files


ADD requirements.txt .
ADD ./app/main.py ./app/
ADD ./app/fix_compiled_path.py ./app/
ADD ./app/houdini_setup_linux.py ./app/
ADD ./app/houdini_setup_mac.py ./app/
ADD ./app/houdini_setup_shared.py ./app/
ADD ./app/houdini_setup_windows.py ./app/
ADD ./app/pysoma_lib.py ./app/
ADD ./app/main_config.yml ./app/
ADD ./app/project_template_master.yml ./app/


#install like from terminal  dependencies
RUN python3 -m venv /opt/venv
# RUN ls ./venv/


COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

WORKDIR /app
COPY . /app

VOLUME /host_files

COPY main.py .


CMD ls .
#run as if in terminal
CMD . /opt/venv/bin/activate && exec python main.py
# CMD ["python", "./main.py"]

