# Bathhouse Employment Contract

An interactive Streamlit app for a Japanese film final project inspired by *Spirited Away*. The app presents a fictional digital contract-signing page where visitors surrender their name, receive a short bathhouse name, and are assigned a bathhouse job role.

The project explores contracts, identity, labor, and spectatorship through an original interface inspired by modern e-signature tools and Japanese bathhouse design details. It avoids copyrighted stills, official logos, and large quoted passages from the film.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy On Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from the repo.
4. Set the main file path to `app.py`.
5. Deploy.

## Files

- `app.py` - Main Streamlit application.
- `requirements.txt` - Lightweight Python dependencies.
- `assets/` - Placeholder for future original images or textures.

## Notes

Name and role assignment are deterministic: the same submitted name should usually receive the same bathhouse name and job role.
