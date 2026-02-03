import requests
import pandas as pd

TAG = "Metroidvania"
URL = f"https://steamspy.com/api.php?request=tag&tag={TAG}"

def start_scouting():
    print(f"正在連線數據庫，分析【{TAG}】標籤下的遊戲資料...")
    
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        gems = []
        blacklist = [
            "legend", "idle", "mmo", "online", "傳說", "仙俠", 
            "掛機", "手游", "mobile", "clicker", "rpgmaker", "batman", "lego"
        ]
        
        for appid, info in data.items():
            name = info.get('name', 'Unknown')
            if any(word in name.lower() for word in blacklist):
                continue
            
            price = int(info.get('price', 0))
            if price == 0:
                continue
                
            pos = info.get('positive', 0)
            neg = info.get('negative', 0)
            total = pos + neg
            
            # 調整評論數上限為 2000 以過濾大作
            if 300 <= total <= 2000:
                score = (pos / total) * 100 if total > 0 else 0
                if score >= 95:
                    img_url = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/header.jpg"
                    
                    gems.append({
                        '縮圖': img_url,
                        '遊戲名稱': name,
                        '好評率_數值': score,
                        '好評率': f"{score:.1f}%",
                        '總評論數': total,
                        '價格': f"${price/100:.2f}",
                        '連結': f"https://store.steampowered.com/app/{appid}"
                    })
        
        if gems:
            df = pd.DataFrame(gems)
            df = df.sort_values(by='好評率_數值', ascending=False)
            
            df.drop(columns=['好評率_數值']).to_csv("gems.csv", index=False, encoding='utf-8-sig')
            
            html_content = """
            <html>
            <head><style>
                body {{ font-family: sans-serif; background: #1b2838; color: white; padding: 20px; }}
                .game-card {{ border: 1px solid #316282; margin-bottom: 10px; padding: 10px; display: flex; align-items: center; background: #2a475e; border-radius: 5px; }}
                img {{ width: 200px; border-radius: 3px; margin-right: 20px; }}
                .info {{ flex-grow: 1; }}
                a {{ color: #66c0f4; text-decoration: none; font-weight: bold; }}
                .score {{ color: #a3da3b; }}
            </style></head>
            <body>
                <h1>搜尋結果：{tag}</h1>
            """.format(tag=TAG)

            for _, row in df.iterrows():
                html_content += f"""
                <div class="game-card">
                    <img src="{row['縮圖']}">
                    <div class="info">
                        <h3>{row['遊戲名稱']}</h3>
                        <p>好評率: <span class="score">{row['好評率']}</span> | 評論數: {row['總評論數']} | 價格: {row['價格']}</p>
                        <a href="{row['連結']}" target="_blank">點此前往商店頁面</a>
                    </div>
                </div>
                """
            
            html_content += "</body></html>"
            
            with open("report.html", "w", encoding="utf-8") as f:
                f.write(html_content)
                
            print(f"完成。已找到 {len(df)} 款遊戲。")
            print("請查看 report.html 確認結果。")
            
        else:
            print("未發現符合條件的遊戲。")
            
    except Exception as e:
        print(f"程式錯誤：{e}")

if __name__ == "__main__":
    start_scouting()