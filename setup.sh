mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"vedikachauhan2002@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml

apt-get update
apt-get install -y tesseract-ocr
