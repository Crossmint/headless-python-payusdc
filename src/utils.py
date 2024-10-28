

def validate(exp, message):
    if not exp:
        raise Exception(message)

base_url = "https://staging.crossmint.com/api/2022-06-09"