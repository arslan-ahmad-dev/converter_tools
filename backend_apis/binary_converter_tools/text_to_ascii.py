import uvicorn
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

class TextToAsciiConverter:
    @staticmethod
    def convert(text_data: str) -> str:
        try:
            ascii_values = [str(ord(char)) for char in text_data]
            return ' '.join(ascii_values)
        except TypeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid input type for text_data: {str(e)}")

@app.post("/convert-text-to-ascii/")
async def convert_text_to_ascii(request: Request):
    try:
        form_data = await request.form()
        text_data = form_data.get("text_data")

        if not text_data:
            raise HTTPException(status_code=400, detail="text_data field is required.")
        
        converter = TextToAsciiConverter()
        ascii_result = converter.convert(text_data)
        return {"ascii": ascii_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
