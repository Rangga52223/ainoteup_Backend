from app.route import authen

@authen.post('/register')
async def register_route():
    