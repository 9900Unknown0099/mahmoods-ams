# Mahmoods AMS Website

Static website for Mahmoods AMS. Built with plain HTML, CSS, and JavaScript; no build step is required.

## Publish with GitHub Pages

Repository: `9900Unknown0099/mahmoods-ams-website`

1. Create a **public** repository named `mahmoods-ams-website` under the GitHub account `9900Unknown0099`.
2. Upload the **contents of this folder** to the repository root. `index.html`, `privacy.html`, `assets/`, `downloads/`, and `.nojekyll` should be directly at the repository root—not inside another nested website folder.
3. Open **Settings → Pages**.
4. Under **Build and deployment**, select **Deploy from a branch**.
5. Select branch `main`, folder `/(root)`, and click **Save**.
6. Wait for the Pages deployment to finish. The expected URL is `https://9900Unknown0099.github.io/mahmoods-ams-website/`.

If you already created the repository, upload these files to it instead of creating a duplicate.

## Optional: GitHub Releases for APK downloads

GitHub Pages hosts the website; GitHub Releases can host versioned APK downloads as a secondary source.

1. Open the repository's **Releases** section and choose **Draft a new release**.
2. Create a tag such as `v1.0.0` and title it `Mahmoods AMS v1.0.0`.
3. Attach the signed release APK as a release asset and publish the release.
4. Copy the release asset's download URL before changing the website's download button. Test that URL in a private/incognito window.

The current site retains its existing APK download path. Do not change it to a release URL until the release asset has actually been published and verified.

## Updating the APK

1. Replace `downloads/Mahmoods-AMS-v1.0.apk` with the new signed APK (or update the filename and all references consistently).
2. Run `python tools/update_checksum.py` from the repository root to refresh checksum/download metadata where supported.
3. Update the version text and links as needed, then commit the changes.

## Security and publishing notes

- Never commit signing keystores, passwords, access tokens, or private configuration files.
- Only distribute APKs signed with the intended release key.
- Review the contact email and privacy-policy statements before public launch.
- All site links are relative so the site can run from a GitHub Pages project subpath.

## Files

- `index.html` — homepage
- `features.html` — features
- `how-it-works.html` — workflow
- `download.html` — downloads and requirements
- `about.html` — about
- `privacy.html` — privacy policy
- `404.html` — not-found page
- `assets/` — CSS, JavaScript, and images
- `downloads/` — current APK
