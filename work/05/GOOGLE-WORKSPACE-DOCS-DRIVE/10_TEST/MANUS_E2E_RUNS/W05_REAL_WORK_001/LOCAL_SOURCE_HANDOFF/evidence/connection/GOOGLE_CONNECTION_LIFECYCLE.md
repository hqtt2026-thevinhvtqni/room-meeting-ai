# Google Connection Lifecycle

| Current state | Event | Next state | Required action |
|---|---|---|---|
| NOT_CONNECTED | connect requested | CONNECTING | issue OAuth state and controlled authorization URL |
| CONNECTING | successful callback and identity | CONNECTED | persist encrypted credential and metadata |
| CONNECTING | invalid state/provider denial/exchange failure | ERROR | keep credential absent; sanitized error |
| CONNECTED | token refresh success | CONNECTED | replace encrypted credential |
| CONNECTED | refresh/revocation/invalid credential failure | REAUTH_REQUIRED | block operations and require reconnect |
| CONNECTED | user disconnect | DISCONNECTED | delete credential and block operations |
| REAUTH_REQUIRED | successful new callback | CONNECTED | replace credential and update metadata |
| DISCONNECTED | reconnect requested | CONNECTING | create a new authorization attempt |

An ERROR state never becomes CONNECTED without a successful authentication callback. Disconnect records an audit event without secret values. Provider revoke is not claimed because no real provider revoke call is implemented.
