{
    "builds": [{
        "src": "ECOM/wsgi.py",
        "use": "@ardnt/vercel-python-wsgi",
        "config": { "maxLambdaSize": "15mb" }
    }],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "ECOM/wsgi.py"
        }
    ]
}