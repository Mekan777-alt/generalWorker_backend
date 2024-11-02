#!/bin/bash

uvicorn src.admin_app:app --host 0.0.0.0 --port 8001 --forwarded-allow-ips='*' --proxy-headers
