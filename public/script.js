fetch('games_data.json')
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById('game-list');
        if (data.length === 0) {
            list.innerHTML = '<p>查無符合條件的遊戲。</p>';
            return;
        }
        
        list.innerHTML = data.map(game => `
            <div class="card">
                <img src="${game.img}">
                <div class="card-content">
                    <h3>${game.name}</h3>
                    <p>好評率: <span class="score">${game.score}</span></p>
                    <p>評論數: ${game.reviews} | 價格: ${game.price}</p>
                    <a href="${game.link}" class="btn" target="_blank">前往商店</a>
                </div>
            </div>
        `).join('');
    })
    .catch(err => {
        document.getElementById('game-list').innerHTML = '<p>讀取數據失敗。</p>';
        console.error('Error loading JSON:', err);
    });