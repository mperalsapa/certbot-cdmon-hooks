#!/bin/bash

certbot certonly \
    --staging \
    --dry-run \
    --manual \
    --manual-auth-hook "./cdmon-letsencrypt.py update" \
    --manual-cleanup-hook "./cdmon-letsencrypt.py cleanup" \
    --preferred-challenges dns \
    -d *.domain.com
    # testing domain