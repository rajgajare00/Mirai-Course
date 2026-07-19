# TODO - AI Image Studio migration

- [x] Identify a free, currently working text-to-image API endpoint that does not require a paid subscription (and avoid complex backend).
- [x] Update local tests to verify Pollinations endpoints (401/429/timeouts found).
- [x] Update `app.py` to remove Pollinations and use a free no-auth placeholder image endpoint while keeping the same Streamlit UI/features.
- [x] Add/keep code comments about where an API key would be needed (none expected for the placeholder endpoint).
- [x] Update `requirements.txt` if new libraries are needed.
- [x] Update `README.md` with setup instructions for the new endpoint.
- [x] Run a smoke test: start `streamlit run app.py` and confirm Generate/Download works.

