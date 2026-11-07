# Password recovery domain update

## Status
Prepared on the session branch only. It is **not deployed** until the founder explicitly uploads the file to `main` and the Appwrite site deploys it.

`domain-update/forgot-password.html` was built from the existing `main` version at commit `d0cf4f00f7af547b689ce086099c3e1a6ca79c91`. Its only content change is the reset destination expression:

```js
const resetURL = new URL("reset-password.html", window.location.href).href;
```

Recovery emails will therefore point to the same site hostname from which the request was made: `anastomosismd.com`, `www.anastomosismd.com`, or the existing `medchanic-md.appwrite.network`. The hostname must be registered as an Appwrite Web platform. The old site and already-issued old-host links must remain active.

This file is based on `main` rather than the session branch's different branded version, to avoid accidentally changing the live logo or other existing content. **Before upload, confirm that `main`'s `forgot-password.html` is still the same version; if it has changed, regenerate the deployment file instead of overwriting newer work.** The session branch's root `forgot-password.html` and `auth.js` have the same URL expression for future work.

## Deployment and test

1. Download **this folder's** `forgot-password.html` from GitHub, not the session branch's root version.
2. In GitHub, upload it to the **repository root** on `main`, replacing the existing file of the same name. This is a founder action; the agent does not push to main.
3. Wait for Appwrite's successful deployment and confirm it serves that new commit before testing.
4. With a test account you control, request a fresh recovery email from the new domain. A fresh root-origin request should lead to `anastomosismd.com`; a fresh www-origin request should lead to `www.anastomosismd.com`. Do not forward or paste the full reset URL, token, email, or password.
5. If safe for the test account, complete a password change and sign in with it; this is the actual end-to-end check. Merely receiving an email or seeing a reset screen does not prove the change works. Keep the legacy Appwrite domain active for existing links.

The existing form intentionally shows the same generic message when the request fails; therefore verify that the email really arrives rather than relying on the confirmation screen. The patch does not change that behavior. Do not test against a primary account unless you are prepared to change its password.

## Local test

From the repo root, `node tests/recovery-url.test.cjs` tests both file versions with a mocked Appwrite account and checks root, www, legacy and preview origins, invalid email handling and the existing generic failure response. This mock test does not call Appwrite or prove real email delivery.
