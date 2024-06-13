# Semantic comparison app

## Getting Started

- First prepare data on Dora.
  ```bash
  Login Dora and go to ETL/ettoday_ad_aws_tooot and press import button.
  ```
- Download and process the initial data.
  ```bash
  python preprocess.py --export_date 'YYYY-MM-DD'
  ```
- Build the app
  ```bash
  docker-compose up -d
  ```
- Activate App from local
  ```bash
  Local: http://localhost:6868
  account: admin
  password: password
  ```
