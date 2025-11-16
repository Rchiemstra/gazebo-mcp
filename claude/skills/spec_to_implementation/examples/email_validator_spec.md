# Email Validator

A Python library for validating email addresses with comprehensive checks.

## Requirements

- Validate email format according to RFC 5322 standards
- Check for common typos (e.g., gmial.com instead of gmail.com)
- Verify domain exists via DNS lookup
- Support bulk validation of email lists
- Provide detailed validation reports

## Constraints

- Must work without external API calls for basic validation
- DNS lookup should be optional and timeout after 2 seconds
- Should handle international email addresses (IDN)

## Inputs

- `email` (str): Email address to validate
- `check_dns` (bool): Whether to perform DNS validation
- `check_typos` (bool): Whether to check for common typos

## Outputs

- `is_valid` (bool): Whether email is valid
- `errors` (list): List of validation errors
- `suggestions` (list): Suggested corrections if typos found

## Examples

```python
from email_validator import validate_email

result = validate_email('user@example.com', check_dns=True)
if result['is_valid']:
    print("Email is valid!")
else:
    print(f"Errors: {result['errors']}")
```

## Dependencies

- None (standard library only)
