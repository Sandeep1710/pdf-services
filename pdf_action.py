from fastapi import FastAPI, File, UploadFile, HTTPException
from PyPDF2 import PdfWriter, PdfReader
from fastapi.responses import StreamingResponse
from io import BytesIO

app = FastAPI()

@app.post("/merge-pdf")
async def merge_pdf(files: list[UploadFile] = File(...)):
        pdf_writer = PdfWriter()
        
        for file in files :
            if not file.filename.endswith(".pdf"):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
            
            reader = PdfReader(file.file)
            print(len(reader.pages))
            for page in reader.pages:
                pdf_writer.add_page(page)
        
        merged_pdf = BytesIO()
        pdf_writer.write(merged_pdf)
        merged_pdf.seek(0)
        
        return StreamingResponse(
                merged_pdf
        )


      