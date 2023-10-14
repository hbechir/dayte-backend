import random

def generate_verification_code():
    # Generate a random 6-digit code
    verification_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
    return verification_code