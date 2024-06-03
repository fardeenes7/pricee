rm -rf .next && vc build && vc deploy --prebuilt
pip install -r requirements.txt
python3 manage.py collectstatic