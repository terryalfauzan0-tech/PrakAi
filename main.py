from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uvicorn

from scraper import scrape_tiktok
from analyzer import analyze_comments

app = FastAPI(title="TikTok Demand & Behavior Insight AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/analyze")
async def analyze_tiktok_url(req: AnalyzeRequest):
    if not req.url:
        raise HTTPException(status_code=400, detail="URL tidak boleh kosong")
        
    try:
        # Scrape data (Hanya Komentar)
        scraped_data = await scrape_tiktok(req.url)
        comments = scraped_data['scraped_comments']
        real_total = scraped_data['real_total_comments']
        
        # Analyze data
        analysis = analyze_comments(comments)
        
        # Update analytics total with official count from metadata
        # Business Estimates (Ekstrapolasi berdasarkan Total Komentar Resmi)
        analysis['analytics']['total'] = real_total
        categories = analysis['analytics']['categories']
        positif_ingin_beli_count = categories['Positif Ingin Beli']
        scraped_count = len(comments)
        
        # Logic: Estimasi pembeli dihitung dengan persentase niat beli dari sampel x total komentar asli
        if scraped_count > 0:
            estimated_buyers = int((positif_ingin_beli_count / scraped_count) * real_total)
        else:
            estimated_buyers = 0
        
        # Logic: Rekomendasi produksi adalah 120% dari estimasi pembeli (Stok Aman + Buffer 20%)
        production_recommendation = int(estimated_buyers * 1.2)
        if estimated_buyers > 0 and production_recommendation <= estimated_buyers:
            production_recommendation = estimated_buyers + 1
        
        # Smart Recommendation Logic
        pertanyaan_count = categories['Pertanyaan']
        negatif_count = categories['Negatif']
        positif_tidak_beli_count = categories['Positif Tidak Beli']
        total = analysis['analytics']['total']
        
        smart_rec = "Strategi sudah cukup baik, pertahankan engagement!"
        if total > 0:
            if (positif_ingin_beli_count / total) > 0.4:
                smart_rec = "Demand sangat tinggi! Segera pastikan ketersediaan stok produk."
            elif (pertanyaan_count / total) > 0.3:
                smart_rec = "Banyak calon pembeli bertanya. Tambahkan informasi harga dan link pembelian di Bio."
            elif (negatif_count / total) > 0.2:
                smart_rec = "Perlu evaluasi kualitas produk atau harga berdasarkan feedback negatif."
            elif (positif_tidak_beli_count / total) > 0.4:
                smart_rec = "Audiens menyukai konten tapi belum terdorong membeli. Tingkatkan Call-to-Action (CTA)."
        
        return {
            "status": "success",
            "data": {
                "comments": analysis['comments'],
                "analytics": analysis['analytics'],
                "business_estimate": {
                    "estimated_buyers": estimated_buyers,
                    "production_recommendation": production_recommendation
                },
                "keyword_insight": analysis['top_keywords'],
                "smart_recommendation": smart_rec
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
