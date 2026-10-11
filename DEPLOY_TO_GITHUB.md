# Deploy Mahmoods AMS Website to GitHub Pages

## Create the repository

Open https://github.com/new while signed in to `9900Unknown0099`.

- Repository name: `mahmoods-ams-website`
- Visibility: Public (required for free GitHub Pages on the standard free plan)
- Do not initialize with a README, license, or `.gitignore` because this package already includes its site files.

Click **Create repository**.

## Upload the site

On the new empty repository page, choose **uploading an existing file**. Extract this ZIP on your computer and open the `mahmoods-ams-website-deploy` folder. Select all files and folders inside it, including `.nojekyll`, then drag them to the GitHub upload area. Commit directly to `main`.

Important: `index.html` must be at the repository root. Do not upload the parent folder itself as a nested directory.

## Enable Pages

Go to **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, then select `main` and `/(root)`, and save. Watch the **Actions** tab for the Pages deployment workflow. Once it succeeds, open:

https://9900Unknown0099.github.io/mahmoods-ams-website/

## Optional APK release mirror

After the website is live, create a GitHub Release from **Releases → Draft a new release**. Use a version tag (for example, `v1.0.0`), attach the signed APK, and publish. Verify the asset download works before adding its URL to the website. The website's existing direct APK download should remain as-is until that test succeeds.

## Quick smoke test

- Homepage loads and CSS/images appear.
- Privacy link opens `privacy.html` and its section navigation works.
- Features, How It Works, About, and Download pages open.
- APK link downloads the expected APK.
- Test on a phone-sized viewport.
