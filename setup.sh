#!/bin/bash
mkdir -p ~/.streamlit/

# Create a default config file if it doesn't exist
if [ ! -f ~/.streamlit/config.toml ]; then
    cat > ~/.streamlit/config.toml <<EOL
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[browser]
serverAddress = "0.0.0.0"
gatherUsageStats = false

[client]
layout = "wide"
EOL
fi
