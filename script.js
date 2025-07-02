// SERVER CONFIGURATION - Global server data
const serverInfo = {
    name: "Diamond Craft SMP",
    version: "1.20.4",
    region: "US-East",
    maxPlayers: 50
};

// DYNAMIC DATABASE - Like Python global variables
const playersDatabase = [
    {
        id: 1,
        nickname: "Steve",
        avatar: "https://minecraft.wiki/images/2/20/Steve_JE2_BE1.png",
        joinDate: "2024-12-15",
        lastSeen: new Date().toISOString(),
        playtimeMinutes: 1250, // Total minutes played
        isOnline: true,
        materials: {
            diamond: 5,
            gold: 12,
            iron: 25,
            coal: 40,
            wood: 100,
            stone: 200
        }
    },
    {
        id: 2,
        nickname: "Alex",
        avatar: "https://minecraft.wiki/images/f/f6/Alex_JE2_BE1.png",
        joinDate: "2024-12-20",
        lastSeen: "2025-01-01T15:30:00.000Z",
        playtimeMinutes: 890,
        isOnline: false,
        materials: {
            diamond: 3,
            gold: 8,
            iron: 30,
            coal: 50,
            wood: 80,
            stone: 150
        }
    },
    {
        id: 3,
        nickname: "Creeper_Hunter",
        avatar: "https://minecraft.wiki/images/0/0a/Creeper_JE4_BE2.png",
        joinDate: "2024-11-10",
        lastSeen: new Date().toISOString(),
        playtimeMinutes: 2100,
        isOnline: true,
        materials: {
            diamond: 8,
            gold: 15,
            iron: 45,
            coal: 60,
            wood: 120,
            stone: 300
        }
    }
];

// Material point values and images
const materialValues = {
    diamond: 100,
    gold: 50,
    iron: 10,
    coal: 5,
    wood: 2,
    stone: 1
};

// Material images (using local files from images folder)
const materialImages = {
    diamond: "./images/materials/diamond.png",
    gold: "./images/materials/gold.png",
    iron: "./images/materials/iron.png",
    coal: "./images/materials/coal.png",
    wood: "./images/materials/wood.png",
    stone: "./images/materials/stone.png"
};

// FUNCTION to create HTML for one player (like Python function)
function createPlayerHTML(player) {
    let materialsHTML = '';
    
    // Loop through all materials for this player
    for (let material in player.materials) {
        const materialImg = materialImages[material] || ''; // Get image URL
        materialsHTML += `
            <div class="material">
                <div class="material-info">
                    <img src="${materialImg}" alt="${material}" class="material-icon" onerror="this.style.display='none'">
                    <span class="material-name">${material.charAt(0).toUpperCase() + material.slice(1)}</span>
                </div>
                <span class="material-count">${player.materials[material]}</span>
            </div>
        `;
    }
    
    return `
        <div class="player" id="player-${player.id}">
            <div class="player-header">
                <img src="${player.avatar}" alt="${player.nickname}" class="player-avatar">
                <div class="player-info">
                    <h2>Player: <span class="nickname">${player.nickname}</span></h2>
                    <div class="player-status">
                        <span class="status-indicator ${player.isOnline ? 'online' : 'offline'}">
                            ${player.isOnline ? '🟢 Online' : '🔴 Offline'}
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="player-stats">
                <div class="stat-item">
                    <span class="stat-label">Joined:</span>
                    <span class="stat-value">${formatDate(player.joinDate)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Playtime:</span>
                    <span class="stat-value">${formatPlaytime(player.playtimeMinutes)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Last Seen:</span>
                    <span class="stat-value">${formatLastSeen(player.lastSeen)}</span>
                </div>
            </div>
            
            <div class="materials">
                ${materialsHTML}
            </div>
            <p class="total-score">Total Score: <span>0</span></p>
            <button class="calculate-score">Calculate Score</button>
        </div>
    `;
}

// FUNCTION to display all players from database
function displayAllPlayers() {
    const scoreboard = document.getElementById('scoreboard');
    const playersCount = document.getElementById('players-count');
    
    // Clear existing content
    scoreboard.innerHTML = '';
    
    // Create HTML for each player in database
    playersDatabase.forEach(player => {
        scoreboard.innerHTML += createPlayerHTML(player);
    });
    
    // Update player count
    playersCount.textContent = playersDatabase.length;
    
    // Add event listeners to calculate buttons
    addCalculateListeners();
}

// FUNCTION to add event listeners to calculate buttons
function addCalculateListeners() {
    const calculateButtons = document.querySelectorAll('.calculate-score');
    calculateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const player = this.closest('.player');
            const playerId = parseInt(player.id.split('-')[1]);
            const playerData = playersDatabase.find(p => p.id === playerId);
            
            let totalScore = 0;
            for (let material in playerData.materials) {
                if (materialValues[material]) {
                    totalScore += materialValues[material] * playerData.materials[material];
                }
            }
            
            player.querySelector('.total-score span').textContent = totalScore;
        });
    });
}

// FUNCTION to add new player to database
function addNewPlayer() {
    // Array of available avatars with names
    const avatarOptions = [
        { name: "Steve", url: "https://minecraft.wiki/images/2/20/Steve_JE2_BE1.png" },
        { name: "Alex", url: "https://minecraft.wiki/images/f/f6/Alex_JE2_BE1.png" },
        { name: "Creeper", url: "https://minecraft.wiki/images/0/0a/Creeper_JE4_BE2.png" },
        { name: "Zombie", url: "https://minecraft.wiki/images/4/4c/Zombie_JE3_BE2.png" },
        { name: "Skeleton", url: "https://minecraft.wiki/images/8/8c/Skeleton_JE4_BE2.png" },
        { name: "Enderman", url: "https://minecraft.wiki/images/5/50/Enderman_JE4_BE2.png" },
        { name: "Spider", url: "https://minecraft.wiki/images/8/85/Spider_JE2_BE1.png" },
        { name: "Witch", url: "https://minecraft.wiki/images/c/c0/Witch_JE2_BE2.png" }
    ];
    
    // Show custom modal for player creation
    showPlayerCreationModal(avatarOptions);
}

// FUNCTION to update server information in the UI
function updateServerInfo() {
    const serverNameElement = document.getElementById('server-name');
    const mainTitleElement = document.getElementById('main-title');
    const currentDateTimeElement = document.getElementById('current-datetime');
    
    // Update server name in the page
    serverNameElement.textContent = serverInfo.name;
    
    // Update main title to include server name
    mainTitleElement.textContent = `${serverInfo.name} - Scoreboard`;
    
    // Update browser tab title
    document.title = `${serverInfo.name} - Scoreboard`;
    
    // Update current date and time
    currentDateTimeElement.textContent = getCurrentDateTime();
}

// Auto-update current time every minute
setInterval(() => {
    updateServerInfo();
}, 60000); // Update every 60 seconds

// HELPER FUNCTIONS for time formatting
function formatPlaytime(minutes) {
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    const days = Math.floor(hours / 24);
    const remainingHours = hours % 24;
    
    if (days > 0) {
        return `${days}d ${remainingHours}h ${remainingMinutes}m`;
    } else if (hours > 0) {
        return `${hours}h ${remainingMinutes}m`;
    } else {
        return `${minutes}m`;
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatLastSeen(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMinutes = Math.floor((now - date) / (1000 * 60));
    
    if (diffMinutes < 1) return "Just now";
    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}h ago`;
    return `${Math.floor(diffMinutes / 1440)}d ago`;
}

function getCurrentDateTime() {
    const now = new Date();
    return now.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// FUNCTION to show player creation modal with avatar dropdown
function showPlayerCreationModal(avatarOptions) {
    const modal = document.getElementById('modal');
    const modalContent = modal.querySelector('.modal-content');
    
    // Create dropdown options HTML
    let avatarOptionsHTML = '';
    avatarOptions.forEach((avatar, index) => {
        avatarOptionsHTML += `
            <option value="${index}" data-url="${avatar.url}">
                ${avatar.name}
            </option>
        `;
    });
    
    // Create modal content
    modalContent.innerHTML = `
        <h2>🎮 Add New Player</h2>
        
        <div class="form-group">
            <label for="player-nickname">Player Nickname:</label>
            <input type="text" id="player-nickname" placeholder="Enter nickname..." maxlength="20">
        </div>
        
        <div class="form-group">
            <label for="avatar-select">Choose Avatar:</label>
            <select id="avatar-select">
                ${avatarOptionsHTML}
            </select>
        </div>
        
        <div class="avatar-preview">
            <h4>Preview:</h4>
            <img id="avatar-preview-img" src="${avatarOptions[0].url}" alt="Avatar Preview">
            <p id="avatar-preview-name">${avatarOptions[0].name}</p>
        </div>
        
        <div class="modal-buttons">
            <button id="create-player-btn" class="create-btn">Create Player</button>
            <button id="cancel-player-btn" class="cancel-btn">Cancel</button>
        </div>
    `;
    
    // Show modal
    modal.style.display = 'flex';
    
    // Add event listeners
    setupModalEventListeners(avatarOptions);
}

// FUNCTION to setup modal event listeners
function setupModalEventListeners(avatarOptions) {
    const modal = document.getElementById('modal');
    const avatarSelect = document.getElementById('avatar-select');
    const previewImg = document.getElementById('avatar-preview-img');
    const previewName = document.getElementById('avatar-preview-name');
    const createBtn = document.getElementById('create-player-btn');
    const cancelBtn = document.getElementById('cancel-player-btn');
    const nicknameInput = document.getElementById('player-nickname');
    
    // Update preview when dropdown changes
    avatarSelect.addEventListener('change', function() {
        const selectedIndex = parseInt(this.value);
        const selectedAvatar = avatarOptions[selectedIndex];
        previewImg.src = selectedAvatar.url;
        previewName.textContent = selectedAvatar.name;
    });
    
    // Create player button
    createBtn.addEventListener('click', function() {
        const nickname = nicknameInput.value.trim() || "Player" + (playersDatabase.length + 1);
        const selectedIndex = parseInt(avatarSelect.value);
        const selectedAvatar = avatarOptions[selectedIndex];
        
        createNewPlayerWithData(nickname, selectedAvatar.url);
        closeModal();
    });
    
    // Cancel button
    cancelBtn.addEventListener('click', closeModal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Focus on nickname input
    nicknameInput.focus();
}

// FUNCTION to create new player with provided data
function createNewPlayerWithData(nickname, avatarUrl) {
    const newPlayer = {
        id: playersDatabase.length + 1,
        nickname: nickname,
        avatar: avatarUrl,
        joinDate: new Date().toISOString().split('T')[0],
        lastSeen: new Date().toISOString(),
        playtimeMinutes: Math.floor(Math.random() * 60) + 10,
        isOnline: Math.random() > 0.5,
        materials: {
            diamond: Math.floor(Math.random() * 10),
            gold: Math.floor(Math.random() * 20),
            iron: Math.floor(Math.random() * 50),
            coal: Math.floor(Math.random() * 80),
            wood: Math.floor(Math.random() * 150),
            stone: Math.floor(Math.random() * 300)
        }
    };
    
    playersDatabase.push(newPlayer);
    displayAllPlayers();
}

// FUNCTION to close modal
function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}

// INITIALIZE - Run when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Update server information first
    updateServerInfo();
    
    // Display all players from database
    displayAllPlayers();
    
    // Show/Hide functionality
    const btnPlayer = document.getElementById('btn-player');
    btnPlayer.addEventListener('click', function() {
        const scoreboard = document.getElementById('scoreboard');
        if (scoreboard.style.display === 'none') {
            scoreboard.style.display = 'grid';
            btnPlayer.textContent = 'Hide Players';
        } else {
            scoreboard.style.display = 'none';
            btnPlayer.textContent = 'Show Players';
        }
    });
    
    // Add new player functionality
    const btnAddPlayer = document.getElementById('btn-add-player');
    btnAddPlayer.addEventListener('click', addNewPlayer);
});
