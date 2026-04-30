OAuth 2.0 Authorization Server
This feature is available from Vikunja 2.3.0 onwards (or unstable builds).
Vikunja can act as an OAuth 2.0 Authorization Server, implementing the Authorization Code flow with mandatory PKCE (Proof Key for Code Exchange, S256 only). This allows native apps and third-party integrations to authenticate users and obtain access tokens without handling user credentials directly.
Key characteristics:
- PKCE is mandatory (S256 method only).
- No client registration is required. The
client\_id
can be any string chosen by the integrator; it must be consistent between the authorization and token exchange steps. - Redirect URIs must use a custom scheme starting with
vikunja-
(for example,vikunja-flutter://callback
). Standardhttp://
andhttps://
URLs are not supported. - All request and response bodies use JSON. Form-encoded requests are not supported.
- There is no consent screen. Authorization is granted automatically once the user is authenticated.
Relevant specifications#
Endpoints#
| Endpoint | Method | Authentication | Purpose |
|---|---|---|---|
/oauth/authorize | Browser navigation | None (frontend route) | User-facing authorization page |
/api/v1/oauth/authorize | POST | JWT Bearer | Creates an authorization code |
/api/v1/oauth/token | POST | None | Exchanges a code for tokens or refreshes tokens |
Authorization flow#
The complete flow consists of four steps:
1. Redirect the user to the authorization page#
Open a browser or webview to the Vikunja instance’s authorization endpoint with the following query parameters:
https:///oauth/authorize
?response\_type=code
&client\_id=
&redirect\_uri=vikunja-flutter://callback
&code\_challenge=
&code\_challenge\_method=S256
&state=
| Parameter | Required | Description |
|---|---|---|
response\_type | Yes | Must be code . |
client\_id | Yes | Any string that identifies your application. Must match at token exchange. |
redirect\_uri | Yes | Where Vikunja redirects after authorization. Must use a vikunja- scheme. |
code\_challenge | Yes | Base64url-encoded SHA-256 hash of the code\_verifier (see RFC 7636 Section 4.2). |
code\_challenge\_method | Yes | Must be S256 . |
state | Recommended | An opaque value to prevent CSRF. Your app should verify it when receiving the callback. |
Vikunja’s frontend handles user login if the user is not already authenticated.
2. Receive the authorization code#
After the user authenticates, Vikunja redirects to your redirect\_uri
with the authorization code and state:
vikunja-flutter://callback?code=&state=
Your application should verify that the returned state
matches the one you sent.
The authorization code is single-use and expires after 10 minutes.
3. Exchange the code for tokens#
Make a POST request to the token endpoint with a JSON body:
curl -X POST https:///api/v1/oauth/token \
-H "Content-Type: application/json" \
-d '{
"grant\_type": "authorization\_code",
"code": "",
"client\_id": "",
"redirect\_uri": "vikunja-flutter://callback",
"code\_verifier": ""
}'
| Field | Required | Description |
|---|---|---|
grant\_type | Yes | Must be authorization\_code . |
code | Yes | The authorization code received in step 2. |
client\_id | Yes | Must match the client\_id used in step 1. |
redirect\_uri | Yes | Must match the redirect\_uri used in step 1. |
code\_verifier | Yes | The original random string used to generate the code\_challenge . |
Response:
{
"access\_token": "",
"token\_type": "bearer",
"expires\_in": 600,
"refresh\_token": ""
}
The expires\_in
value is configured server-side via the service.jwtttlshort
setting (default: 600 seconds).
4. Refresh the access token#
When the access token expires, use the refresh token to obtain a new one:
curl -X POST https:///api/v1/oauth/token \
-H "Content-Type: application/json" \
-d '{
"grant\_type": "refresh\_token",
"refresh\_token": ""
}'
Response:
The response has the same format as the token exchange response, including a new refresh\_token
. Refresh tokens are rotated on each use — the previous refresh token becomes invalid after a successful refresh.
Generating the PKCE code challenge#
If your OAuth library does not handle PKCE automatically, here is how to generate the values:
- Create a
code\_verifier
: a cryptographically random string between 43 and 128 characters, using characters[A-Z] / [a-z] / [0-9] / - / . / \_ / ~
. - Compute the
code\_challenge
: take the SHA-256 hash of thecode\_verifier
, then base64url-encode it (without padding).
See RFC 7636 Section 4.1 and Section 4.2 for the full specification.
Error codes#
All errors are returned as HTTP 400 responses with a JSON body containing a code
field. See the OAuth section of the error codes reference for the full list.
