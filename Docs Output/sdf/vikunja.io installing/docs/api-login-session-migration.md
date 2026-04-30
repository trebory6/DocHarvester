API login session migration
API Migration Guide: Session-Based Authentication#
Starting in Vikunja 2.0.0, Vikunja’s authentication model moved from long-lived JWTs (72h / 30 days) to short-lived JWTs (10 minutes) paired with server-side sessions and rotating refresh tokens.
The refresh token is delivered as an HttpOnly
cookie and must be sent back on refresh requests. The server rotates the refresh token on every use.
While Vikunja’s first party web frontend works as before, this change will need updates in third-party integrations.
Who Is Affected#
| Client type | Affected? | Action needed |
|---|---|---|
API tokens (tk\_ prefix) | No | No changes. API tokens continue to work as before. |
| Browser-based clients | Yes | Must implement a refresh loop. The cookie is handled automatically by the browser. |
| Non-browser clients (mobile, CLI, scripts) | Yes | Must capture the Set-Cookie header and replay the cookie on refresh requests. |
| Link share tokens | No | Link share JWTs still renew via POST /user/token as before. |
Breaking Changes#
1. JWTs Now Expire in ~10 Minutes#
User JWTs now have a short TTL controlled by service.jwtttlshort
(default: 600 seconds). Clients must refresh the token before it expires.
The exp
claim in the JWT indicates when it expires. Refresh proactively before this time.
2. POST /user/token
No Longer Works for User Tokens#
This endpoint now returns 400 Bad Request
for user JWTs:
{
"message": "User tokens cannot be renewed via this endpoint. Use POST /user/token/refresh with a refresh token."
}
It still works for link share tokens.
3. New Refresh Endpoint: POST /user/token/refresh
#
This is the new way to renew user JWTs. It does not use a Bearer token. Instead, it reads the refresh token from an HttpOnly
cookie.
Request:
POST /api/v1/user/token/refresh
Cookie: vikunja\_refresh\_token=
Response (200):
{
"token": ""
}
The response also includes a Set-Cookie
header with a new refresh token (the old one is invalidated). You must store the new cookie for subsequent refreshes.
Error responses (401):
"No refresh token provided."
— Cookie missing"Invalid or expired refresh token."
— Token not found in database"Session expired."
— Session exceeded its max idle time"Refresh token already used."
— Another request already rotated this token (concurrent refresh race)
4. Login Now Sets a Refresh Token Cookie#
POST /login
still returns {"token": "..."}
in the response body, but it also sets a Set-Cookie
header:
Set-Cookie: vikunja\_refresh\_token=; Path=/api/v1/user/token/refresh; HttpOnly; Secure; SameSite=Strict; Max-Age=259200
Non-browser clients must:
- Parse the
Set-Cookie
header from the login response - Store the cookie value
- Send it as
Cookie: vikunja\_refresh\_token=
on calls toPOST /api/v1/user/token/refresh
5. Refresh Tokens Rotate on Every Use#
Each call to /user/token/refresh
invalidates the old refresh token and returns a new one. You must always use the latest cookie value. Replaying an old token returns 401.
6. Password Changes Invalidate All Sessions#
After POST /user/password
(authenticated password change) or POST /user/password/reset
(forgot password flow), all sessions for that user are deleted. All refresh tokens become invalid and all clients must re-authenticate.
New Endpoints#
POST /user/logout
#
Destroys the current session server-side and clears the refresh token cookie.
Request: Requires a valid JWT in the Authorization
header.
Response (200):
{
"message": "Successfully logged out."
}
You should call this endpoint when your integration logs the user out.
GET /user/sessions
#
Returns a paginated list of active sessions for the authenticated user.
Response (200):
[
{
"id": "550e8400-e29b-41d4-a716-446655440000",
"device\_info": "Mozilla/5.0 ...",
"ip\_address": "192.168.1.1",
"last\_active": "2026-02-25T10:00:00Z",
"created": "2026-02-24T08:00:00Z"
}
]
DELETE /user/sessions/:session
#
Revokes a specific session by its UUID. The session must belong to the authenticated user.
Response (200):
{
"message": "Successfully deleted."
}
JWT Changes#
User JWTs now include two additional claims:
| Claim | Type | Description |
|---|---|---|
sid | string | Session UUID. Ties the JWT to a server-side session. |
jti | string | Unique token ID (UUID). Makes every issued JWT unique. |
Existing claims (type
, id
, username
, exp
) are unchanged.
Error Response Change#
The 401
response for expired or invalid JWTs now returns a structured JSON body with error code 11
:
{
"code": 11,
"message": "missing, malformed, expired or otherwise invalid token provided"
}
Use "code": 11
to distinguish “token expired, try refreshing” from other 401
errors (wrong password, disabled account, etc.).
Example: Non-Browser Client Flow#
1. POST /api/v1/login {"username": "...", "password": "..."}
-> Save response.token as JWT
-> Save Set-Cookie header value for vikunja\_refresh\_token
2. Use JWT in Authorization: Bearer  for API requests
3. When JWT is about to expire (check `exp` claim), or on 401 with code 11:
POST /api/v1/user/token/refresh
Cookie: vikunja\_refresh\_token=
-> Save new response.token as JWT
-> Save new Set-Cookie header value (token was rotated)
4. To log out:
POST /api/v1/user/logout
Authorization: Bearer
