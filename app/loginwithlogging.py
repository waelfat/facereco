import logging
from fastapi import  Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback

# Configure logging to write to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named app.log
        logging.StreamHandler()          # Also log to the console
    ]
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)


# Middleware to log incoming requests and handle exceptions
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        url = str(request.url)
        headers = dict(request.headers)
        query_string = str(request.query_params)

        log_info(f"Incoming request: method={method}, url={url}, headers={headers}, query_string={query_string}")

        try:
            response = await call_next(request)
         # Log error responses 
            return response
        except HTTPException as e:
            # Log the detailed HTTPException information
            error_message = f"HTTPException occurred while handling request {url}: {str(e.detail)} (status code: {e.status_code})"
            log_error(error_message)
            raise e
        except Exception as e:
            # Log generic exception information
            error_message = f"Error occurred while handling request {url}: {str(e)}\n{traceback.format_exc()}"
            log_error(error_message)
            response_message = {"message": "Internal server error. Please try again later."}
            log_error(f"Response to client: {response_message}")
            return JSONResponse(
                status_code=500,
                content=response_message,
            )


