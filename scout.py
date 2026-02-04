import requests
import json

#設定
TAG = "Metroidvania"
URL = f"https://steamspy.com/api.php?request=tag&tag={TAG}"

def start_scouting():
    print(f"正在分析【{TAG}】標籤下的遊戲...")
    
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        gems = []
        # 黑名單過濾大作與不相關類型
        blacklist = ["legend", "idle", "mmo", "online", "傳說", "仙俠", "lego", "rpgmaker"]
        
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
            
            # 評論數門檻與好評率過濾
            if 300 <= total <= 2000:
                score = (pos / total) * 100 if total > 0 else 0
                if score >= 95:
                    gems.append({
                        "name": name,
                        "score": f"{score:.1f}%",
                        "reviews": total,
                        "price": f"${price/100:.2f}",
                        "link": f"https://store.steampowered.com/app/{appid}",
                        "img": f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/header.jpg"
                    })
        
        # 排序：好評率高到低
        gems.sort(key=lambda x: float(x['score'].replace('%', '')), reverse=True)

        # 儲存為 JSON
        with open("public/games_data.json", "w", encoding="utf-8") as f:
            json.dump(gems, f, ensure_ascii=False, indent=4)
        
        print(f"完成。已找到 {len(gems)} 款遊戲，數據已更新至 games_data.json")

    except Exception as e:
        print(f"程式執行錯誤：{e}")

if __name__ == "__main__":
    start_scouting()