FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY guardrails_mcp ./guardrails_mcp
RUN pip install --no-cache-dir '.[dashboard]' && useradd --create-home runner && mkdir /data && chown runner:runner /data
USER runner
ENV GUARDRAILS_DATA_DIR=/data GUARDRAILS_HOST=0.0.0.0 GRADIO_ANALYTICS_ENABLED=False
EXPOSE 7861
CMD ["guardrails-dashboard"]
