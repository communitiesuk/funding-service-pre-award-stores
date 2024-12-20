FLASK_APP=app:create_app
FLASK_ENV=development
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=localhost
# Below credentials belongs to local development server. Do not commit any external services credentials
DATABASE_URL=postgresql://postgres:password@localhost:5432/pre_award_stores # pragma: allowlist secret
FUND_STORE_API_HOST=http://localhost:3012/fund
ACCOUNT_STORE_API_HOST=http://localhost:3012/account
APPLICATION_STORE_API_HOST=http://localhost:3012/application
AWS_ACCESS_KEY_ID=FSDIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=fsdlrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY # pragma: allowlist secret
AWS_BUCKET_NAME=fsd-bucket
AWS_ENDPOINT_OVERRIDE=http://localhost:4566
AWS_REGION=eu-west-2

SQLALCHEMY_WARN_20=1
