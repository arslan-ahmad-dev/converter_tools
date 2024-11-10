import uvicorn
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

class AsciiToTextConverter:
    @staticmethod
    def convert(ascii_data: str) -> str:
        try:
            ascii_values = ascii_data.split()
            text_result = ''.join(chr(int(value)) for value in ascii_values)
            return text_result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid ASCII data format: {str(e)}")

@app.post("/convert-ascii-to-text/")
async def convert_ascii_to_text(request: Request):
    try:
        form_data = await request.form()
        ascii_data = form_data.get("ascii_data")

        if not ascii_data:
            raise HTTPException(status_code=400, detail="ascii_data field is required.")
        
        converter = AsciiToTextConverter()
        text_result = converter.convert(ascii_data)
        return {"text": text_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
