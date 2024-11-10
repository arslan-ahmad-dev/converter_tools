import uvicorn
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

class BinaryToHexConverter:
    @staticmethod
    def convert(binary_data: str) -> str:
        try:
            binary_values = binary_data.split(' ')
            hex_values = [hex(int(bv, 2))[2:].upper() for bv in binary_values]
            return ' '.join(hex_values)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid binary data format: {str(e)}")

@app.post("/convert-binary-to-hex")
async def convert_binary_to_hex(request: Request):
    try:
        form_data = await request.form()
        binary_data = form_data.get("binary_data")

        if not binary_data:
            raise HTTPException(status_code=400, detail="binary_data field is required.")
        
        converter = BinaryToHexConverter()
        hex_result = converter.convert(binary_data)
        return {"hex": hex_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
