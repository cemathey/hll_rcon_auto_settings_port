# FROM python:3.11-buster as tag_version
FROM python:3.11-buster

WORKDIR /code
# COPY .git/ .git/
# RUN git describe --tags > /code/tag_version
# RUN rm -r .git

# FROM python:3.11-slim-buster

ARG APP_NAME=hll_rcon_auto_settings_port

WORKDIR /code
RUN apt update -y \
    && apt upgrade --no-install-recommends -y \ 
    curl \
    pipx \
    python3-venv
RUN pipx ensurepath
RUN pipx install poetry
RUN pip install gunicorn
ENV PATH="/root/.local/bin:$PATH"
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY ./${APP_NAME} ${APP_NAME}
COPY ./entrypoint.sh entrypoint.sh
# COPY --from=tag_version /code/tag_version /code/tag_version

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/code/entrypoint.sh" ]