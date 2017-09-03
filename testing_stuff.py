from app import app

client = app.test_client()

response = client.post('/', data=dict(
        telephone='+18059011596',
    ), follow_redirects=True)

print(response.data)

