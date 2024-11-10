import uvicorn
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

class DecimalToHexadecimalConverter:
    @staticmethod
    def convert(decimal_data: str) -> str:
        try:
            decimal_value = int(decimal_data)
            return hex(decimal_value)[2:]
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid decimal data format: {str(e)}")

@app.post("/convert-decimal-to-hexadecimal/")
async def convert_decimal_to_hexadecimal(request: Request):
    try:
        form_data = await request.form()
        decimal_data = form_data.get("decimal_data")

        if not decimal_data:
            raise HTTPException(status_code=400, detail="decimal_data field is required.")
        
        converter = DecimalToHexadecimalConverter()
        hexadecimal_result = converter.convert(decimal_data)
        return {"hexadecimal": hexadecimal_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
