from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Production entry point - add your application initialization here

if __name__ == "__main__":
    uvicorn.run("app.api.v1.api:app", host="0.0.0.0", port=8000, reload=True)