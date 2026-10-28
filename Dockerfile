FROM python:3.11-slim

WORKDIR /app

# Copy scripts and datasets
COPY order_analyzer.py /app/
COPY validator_scanner.py /app/
COPY analysis_results.json /app/
COPY observed_validators.json /app/
COPY INSIDE_THE_BLOCK_RESEARCH_REPORT.md /app/
COPY README.md /app/

# Environment defaults (Dry run enabled by default, zero risk)
ENV PYTHONUNBUFFERED=1

CMD ["python", "order_analyzer.py", "--dry-run"]
