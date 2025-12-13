import secrets

print("\n=== Secure Keys for Production ===\n")
print("SECRET_KEY:")
print(secrets.token_urlsafe(32))
print("\nJWT_SECRET_KEY:")
print(secrets.token_urlsafe(32))
print("\n=== Save these keys securely! ===\n")
