import uvicorn
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

class TextToBinaryConverter:
    @staticmethod
    def convert(text: str) -> str:
        try:
            binary_values = [format(ord(char), '08b') for char in text]
            return ' '.join(binary_values)
        except TypeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid input type for text: {str(e)}")

@app.post("/convert-text-to-binary")
async def convert_text_to_binary(request: Request):
    try:
        form_data = await request.form()
        text = form_data.get("text")

        if not text:
            raise HTTPException(status_code=400, detail="text field is required.")
        
        converter = TextToBinaryConverter()
        binary_result = converter.convert(text)
        return {"binary": binary_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
