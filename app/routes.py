from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import requests
from urllib.parse import quote

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return """  
<!DOCTYPE html>  
<html>  
<head>  
    <title>ComicCraft AI</title>  
    <script src="https://cdn.tailwindcss.com"></script>  
</head>  
<body class="relative h-screen bg-cover bg-center flex items-center justify-center overflow-hidden"  
      style="background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1920&auto=format&fit=crop');">  
    <div class="absolute inset-0 bg-black/15"></div>  
    <div class="relative z-10 bg-white/95 backdrop-blur-md p-6 rounded-xl shadow-2xl w-[420px] border border-white/20">  
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">  
            ✏️ Create Your Comic  
        </h2>  
        <form action="/generate" method="post" class="space-y-3">  
            <div>  
                <label class="block text-[11px] font-bold uppercase tracking-wider text-gray-700 mb-1">Story Prompt:</label>  
                <textarea name="story" rows="3" class="w-full border border-gray-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-blue-500 outline-none bg-white" placeholder="A brave fox explores an enchanted forest." required></textarea>  
            </div>  
            <div>  
                <label class="block text-[11px] font-bold uppercase tracking-wider text-gray-700 mb-1">Main Character Name:</label>  
                <input type="text" name="character" class="w-full border border-gray-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-blue-500 outline-none bg-white" value="Maya">  
            </div>  
            <div>  
                <label class="block text-[11px] font-bold uppercase tracking-wider text-gray-700 mb-1">Setting:</label>  
                <select name="setting" class="w-full border border-gray-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-blue-500 outline-none bg-white">  
                    <option value="Forest">Forest</option>  
                    <option value="City">City</option>  
                    <option value="Space">Space</option>  
                    <option value="Castle">Castle</option>  
                </select>  
            </div>  
            <div>  
                <label class="block text-[11px] font-bold uppercase tracking-wider text-gray-700 mb-1">Story Tone:</label>  
                <select name="tone" class="w-full border border-gray-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-blue-500 outline-none bg-white">  
                    <option value="Dramatic">Dramatic</option>  
                    <option value="Comic">Comic</option>  
                    <option value="Adventure">Adventure</option>  
                    <option value="Mystery">Mystery</option>  
                </select>  
            </div>  
            <div>  
                <label class="block text-[11px] font-bold uppercase tracking-wider text-gray-700 mb-1">Art Style:</label>  
                <select name="style" class="w-full border border-gray-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-blue-500 outline-none bg-white">  
                    <option value="Realistic">Realistic</option>  
                    <option value="Anime">Anime</option>  
                    <option value="Pixel Art">Pixel Art</option>  
                    <option value="Classic Comic">Classic Comic</option>  
                </select>  
            </div>  
            <button type="submit" class="w-full bg-[#0095ff] hover:bg-blue-600 text-white font-semibold py-2.5 rounded-lg shadow transition duration-200 text-sm mt-1">  
                Generate Comic  
            </button>  
        </form>  
    </div>  
</body>  
</html>  
"""

@router.post("/generate", response_class=HTMLResponse)
def generate_comic(
    request: Request, 
    story: str = Form(...), 
    character: str = Form(""), 
    setting: str = Form(""), 
    tone: str = Form(""), 
    style: str = Form("")
):
    try:
        combined_prompt = f"{story}, Character: {character}, Setting: {setting}, Tone: {tone}, Style: {style}"
        
        panels_dir = "app/static/panels"
        os.makedirs(panels_dir, exist_ok=True)
        
        panels = []
        for i in range(1, 6):
            filename = f"panel_{i}.jpg"
            file_path = os.path.join(panels_dir, filename)
            
            # Panel-specific prompt for AI image generation
            panel_prompt = f"Panel {i} of a comic strip: {combined_prompt}, comic book art style"
            encoded_prompt = quote(panel_prompt)
            
            # Real AI Image Generation using Pollinations AI
            img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=600&height=600&nologo=true"
            
            response = requests.get(img_url, timeout=30)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
            
            panels.append({
                "panel": i, 
                "text": f"Panel {i}: {combined_prompt}", 
                "image_path": f"/static/panels/{filename}"
            })
            
        return templates.TemplateResponse(
            request, 
            "comic_preview.html", 
            {"panels": panels}
        )
    except Exception as e:
        return HTMLResponse(content=f"<h3 style='color:red; padding:20px;'>Error: {str(e)}</h3>", status_code=500)
        