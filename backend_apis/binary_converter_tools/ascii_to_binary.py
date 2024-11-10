import uvicorn
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

class AsciiToBinaryConverter:
    @staticmethod
    def convert(ascii_text: str) -> str:
        try:
            binary_values = [format(ord(char), '08b') for char in ascii_text]
            return ' '.join(binary_values)
        except TypeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid input type for ascii_text: {str(e)}")

@app.post("/convert-ascii-to-binary/")
async def convert_ascii_to_binary(request: Request):
    try:
        form_data = await request.form()
        ascii_text = form_data.get("ascii_text")

        if not ascii_text:
            raise HTTPException(status_code=400, detail="ascii_text field is required.")
        
        converter = AsciiToBinaryConverter()
        binary_result = converter.convert(ascii_text)
        return {"binary": binary_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
