# Security notes

This prototype includes basic web security appropriate for local development, not a certified hospital deployment.

Included:
- Password hashing using Werkzeug scrypt
- CSRF protection
- HttpOnly cookies
- SameSite=Lax session cookies
- Login audit events
- Patient audit events
- No patient data in URL query parameters
- Server-side prediction
- SQLite local persistence

Required before real deployment:
- HTTPS only
- Secure cookie flag behind HTTPS
- MFA or hospital SSO
- Strict RBAC
- Per-hospital tenant isolation
- PostgreSQL
- Encryption at rest
- Centralized audit log
- Rate limiting
- Account lockout / abuse monitoring
- Secret manager
- Dependency and container scanning
- Backup and recovery
- Security testing / penetration testing
- Clinical governance and regulatory review
