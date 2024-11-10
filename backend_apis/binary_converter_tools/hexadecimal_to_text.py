import uvicorn
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

class HexadecimalToTextConverter:
    @staticmethod
    def convert(hex_data: str) -> str:
        try:
            bytes_object = bytes.fromhex(hex_data)
            return bytes_object.decode("utf-8")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid hexadecimal data format: {str(e)}")
        except UnicodeDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Hexadecimal data could not be decoded to text: {str(e)}")

@app.post("/convert-hexadecimal-to-text/")
async def convert_hexadecimal_to_text(request: Request):
    try:
        form_data = await request.form()
        hex_data = form_data.get("hex_data")

        if not hex_data:
            raise HTTPException(status_code=400, detail="hex_data field is required.")
        
        converter = HexadecimalToTextConverter()
        text_result = converter.convert(hex_data)
        return {"text": text_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
