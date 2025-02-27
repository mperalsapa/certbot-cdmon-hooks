# Doc

In order to perform Letsencrypt DNS challenges, the requested zone, requires to have a `_acme-challenge` txt record with a token as value.
This script adds support to [cdmon](https://www.cdmon.com/).

# Usage
Simply use certbot as you would usually do, but pass two new parameters 

```bash
# Example command
certbot certonly \
    --manual \
    --manual-auth-hook "./cdmon-letsencrypt.py update" \
    --manual-cleanup-hook "./cdmon-letsencrypt.py cleanup" \
    --preferred-challenges dns \
    -d *.domain
```
# Hooks explanation
For a deeper understanding go to the [official Letsencrypt documentation](https://eff-certbot.readthedocs.io/en/latest/using.html#hooks)
- --manual-auth-hook
    This parameter gets called previous to the `_acme-challenge` value check.
- --manual-cleanup-hook
    This parameter gets called after the `_acme-challenge` value check, so we can do clean jobs (f.e erasing the record)

Each of the previous hooks, call the script passing **env** variables (domain, token, etc...)
