# Manual OAuth completion (when `mcp login` dies before showing a URL)

## When to Use

The login command prints 'no OAuth token was obtained' without ever
printing an authorization URL, even with client_id/secret saved and scopes
corrected. The failure is upstream of the browser step, so retrying the
same command cannot work.

## Diagnose in order, cheapest first

- Confirm the provider actually supports the flow: fetch its
  `/.well-known/oauth-authorization-server` and check for a
  `registration_endpoint` (dynamic registration) plus the real
  `scopes_supported` list. Requesting scopes the provider does not define
  (e.g. openid-style scopes against a provider with its own scope names)
kills the flow before any URL is shown — mirror the provider's scope names
exactly in the server config.
- Confirm the registered redirect matches the client's bound pattern
  exactly (scheme, host, port, path). A bare loopback registration against
a client that binds `http://127.0.0.1:{port}/callback` fails every grant.
Pin a fixed port in config when the client supports it, register that exact
URI, then retry once.
- Prove the provider side with a hand-built authorize URL (fresh PKCE
  pair, saved client_id, exact redirect, provider scopes): landing on the
  provider's consent page means the registration is fine and the blockage
  is inside the client's handshake, not the provider.

## Finish by hand when the client stays blind

- Run your own one-shot listener on the registered port, print the
  authorize URL for the user to open, capture the `code` from the
  redirect, and exchange it at the token endpoint (PKCE verifier +
  client_secret).
- Store the result in the client's native token file format (access_token,
  token_type, expires_in, scope, refresh_token, expires_at, issuer) plus
  the companion metadata file the client expects next to it; 0600 perms.
- Update the cached client registration to the same client_id BEFORE
  storing tokens or testing: on a mismatch the client's manager purges
  the stored tokens as foreign and the next test reports no cached
  tokens. Registration file first, tokens second, test third — that order
  is load-bearing.
- Re-test through the client's own `mcp test`, then delete the one-shot
  scripts. The stored tokens (plus refresh) make the door native — the
  broken helper is bypassed, not the auth itself.
- Renaming a registered OAuth client is re-registration, not an edit: no
  provider exposes a rename endpoint (probe first — a 404/405 on any
  client-management path confirms it), so register the new name, complete
a fresh grant, verify, then revoke the old grant. Never reuse the old
tokens under the new name.
