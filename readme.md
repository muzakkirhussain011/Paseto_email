# Paseto Email Demo

This repository contains two simple services used to demonstrate issuing
PASETO tokens and sending e-mail based one-time passwords (OTP).

* `api2_token_email.py` – a FastAPI microservice that generates tokens and
  sends e-mails. It expects environment variables for AWS SES and a symmetric
  key. Endpoints are protected by `X-API-Key`.
* `api1_springboot` – a minimal Spring Boot application used to test API-2.
  It exposes `/api/register`, `/api/verify`, `/api/login` and `/api/ping` and
  serves a static `index.html` to exercise the flow.

The Spring Boot app keeps OTPs in memory and uses hard coded values to call
API‑2. Use this only for local experiments.
