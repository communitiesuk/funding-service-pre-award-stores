FLASK_APP=app:application
FLASK_ENV=development
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=localhost
# Below credentials belongs to local development server. Do not commit any external services credentials
DATABASE_URL=postgresql://postgres:password@localhost:5432/pre_award_stores # pragma: allowlist secret
FUND_STORE_API_HOST=http://localhost:3012/fund
ACCOUNT_STORE_API_HOST=http://localhost:3003
APPLICATION_STORE_API_HOST=http://localhost:3012/application
AWS_ACCESS_KEY_ID=FSDIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=fsdlrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY # pragma: allowlist secret
AWS_BUCKET_NAME=fsd-bucket
AWS_ENDPOINT_OVERRIDE=http://localhost:4566
AWS_REGION=eu-west-2
AWS_DLQ_MAX_RECIEVE_COUNT=3
AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL=http://localhost:4566/000000000000/import-queue.fifo
AWS_SQS_IMPORT_APP_SECONDARY_QUEUE_URL=http://localhost:4566/000000000000/import-queue-dlq.fifo

SQLALCHEMY_WARN_20=1
