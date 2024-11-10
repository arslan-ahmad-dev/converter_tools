import uvicorn
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

class HexToBinaryConverter:
    @staticmethod
    def convert(hex_data: str) -> str:
        try:
            hex_values = hex_data.split(' ')
            binary_values = [format(int(hv, 16), '04b') for hv in hex_values]
            return ' '.join(binary_values)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid hexadecimal data format: {str(e)}")

@app.post("/convert-hex-to-binary/")
async def convert_hex_to_binary(request: Request):
    try:
        form_data = await request.form()
        hex_data = form_data.get("hex_data")

        if not hex_data:
            raise HTTPException(status_code=400, detail="hex_data field is required.")
        
        converter = HexToBinaryConverter()
        binary_result = converter.convert(hex_data)
        return {"binary": binary_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
