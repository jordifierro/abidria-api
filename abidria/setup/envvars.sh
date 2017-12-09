#!/bin/bash
# Local development env vars 
export DEBUG='1'
export LOCAL_DEPLOY='1'

export DATABASE_NAME='abidria_db'
export DATABASE_USER='abidria_user'
export DATABASE_PASS='password'

export SECRET_KEY='39#j7n^$06yb=t-3u!-h(q)25sq&_2_hwq8zw@*r5p%tu=y1uj'
export CLIENT_SECRET_KEY='299d43b710b142b4bc7d5d62772acfa9'

export EMAIL_USE_TLS='1'
export EMAIL_HOST='smtp.example.com' 
export EMAIL_HOST_PASSWORD='my_secret_password'
export EMAIL_HOST_USER='email@example.com'
export EMAIL_PORT='123'

# Remote deployment extra env vars
# export ALLOWED_HOSTS='example.com'
# export AWS_ACCESS_KEY_ID='amazon_key'
# export AWS_SECRET_ACCESS_KEY='amazon_secret'
# export AWS_STORAGE_BUCKET_NAME='abidria-bucket'
# export DATABASE_URL='postgres://amazonaws.com'
