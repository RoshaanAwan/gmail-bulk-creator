# Security Policy

## Reporting Security Vulnerabilities

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them to security@example.com. Please include:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if available)

We will acknowledge receipt of your report within 48 hours and provide regular updates on our progress.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Yes    |
| < 1.0   | ❌ No     |

## Security Best Practices

When using Gmail Bulk Creator, please follow these security practices:

1. **Environment Variables**
   - Never commit `.env` files with real credentials
   - Use `.gitignore` to exclude sensitive files
   - Consider using a secrets manager

2. **Password Security**
   - Use strong, unique passwords for accounts
   - Never hardcode passwords in scripts
   - Store passwords securely

3. **Proxy Usage**
   - Use trusted proxy services
   - Validate proxy connections
   - Monitor for suspicious activity

4. **Data Protection**
   - Protect CSV files containing account information
   - Restrict file access to authorized users only
   - Consider encrypting sensitive data

5. **Compliance**
   - Ensure usage complies with Google's Terms of Service
   - Follow local laws and regulations
   - Document the purpose of bulk account creation
   - Maintain audit logs

## Dependencies

This project uses the following dependencies:
- Selenium: WebDriver automation
- webdriver-manager: Chrome driver management
- python-dotenv: Environment configuration
- openpyxl: Excel file handling
- requests: HTTP library
- google-auth libraries: Google API authentication

We regularly monitor these dependencies for security updates.

## Disclaimer

This tool is provided for educational and legitimate business purposes. Users are responsible for ensuring their use complies with all applicable laws, regulations, and terms of service.

Unauthorized account creation may violate:
- Google's Terms of Service
- Computer fraud laws
- Local regulations on account creation

Use responsibly and legally.
