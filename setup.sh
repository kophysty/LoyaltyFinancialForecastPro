#!/bin/bash
mkdir -p ~/.streamlit/
echo "\
[server]\nport = $PORT\nenableCORS = false\nenableXsrfProtection = true\nmaxUploadSize = 200\n\n[browser]\nserverAddress = \"0.0.0.0\"\ngatherUsageStats = false\n" > ~/.streamlit/config.toml
