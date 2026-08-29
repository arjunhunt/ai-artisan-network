/* ==============================================================================
   AI ARTISAN COMMERCE NETWORK - MASTER FRONTEND CONTROLLER (JAVASCRIPT)
   Smart India Hackathon 2026 Prototype
   ============================================================================== */

let currentUser = {
  id: 1,
  name: "Rishikant Mishra",
  role: "ARTISAN",
  identifier: "DEMO-ARTISAN-001"
};

let currentOrdersFilter = 'my'; // 'my' or 'all'
let currentUploadedImageUrl = null;
let currentCart = JSON.parse(localStorage.getItem('artisan_cart') || '[]');
let currentWishlist = JSON.parse(localStorage.getItem('artisan_wishlist') || '[]');
let isRecording = false;
let recognition = null;
let currentExtractedData = null;
let currentPricingData = null;
let activeChatOrderId = 1;

// --- ELEGANT TOAST NOTIFICATION SYSTEM (Bottom Green Toast) ---
function showToast(message, type = 'success', duration = 2000) {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast-message toast-${type}`;
  
  let icon = '🎉';
  if (type === 'info') icon = 'ℹ️';
  if (type === 'warning') icon = '⚠️';
  if (type === 'danger') icon = '❌';
  if (message.includes('❤️') || message.includes('Wishlist')) icon = '';
  if (message.includes('💾')) icon = '';

  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('toast-hiding');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

function saveCart() {
  localStorage.setItem('artisan_cart', JSON.stringify(currentCart));
  updateCartBadge();
}

function updateCartBadge() {
  const totalCount = currentCart.reduce((sum, it) => sum + (it.quantity || 1), 0);
  const badge = document.getElementById('cartCount');
  if (badge) badge.innerText = totalCount;
}

function updateWishlistBadge() {
  const badge = document.getElementById('wishlistCount');
  if (badge) badge.innerText = currentWishlist.length;
}

// 8 Authentic SIH Demo Craft Presets (Local Offline-Ready Assets)
const CRAFT_PRESETS = {
  paithani: {
    artisan: "Rishikant Mishra",
    state: "Maharashtra",
    image: "/static/images/product_1.svg",
    category: "Handloom & Silk",
    title: "Authentic Handwoven Paithani Silk Saree",
    transcript: "Ye hamne pure mulberry silk aur golden zari se banaya hai. Peacock mor motif weave karne me 15 ghante lage.",
    material: 800,
    hours: 15,
    margin: 20,
    intended: 900,
    gi_number: "GI-MH-001"
  },
  madhubani: {
    artisan: "Meenakshi Jha",
    state: "Bihar",
    image: "/static/images/product_11.svg",
    category: "Folk Art & Decor",
    title: "Traditional Madhubani Mithila Tree of Life Painting",
    transcript: "Mithila folk art painting on handmade paper depicting Tree of Life and sacred fish using natural vegetable dyes over 8 hours.",
    material: 350,
    hours: 8,
    margin: 25,
    intended: 1220,
    gi_number: "GI-BR-002"
  },
  blue_pottery: {
    artisan: "Devendra Sharma",
    state: "Rajasthan",
    image: "/static/images/product_21.svg",
    category: "Ceramics & Decor",
    title: "Handcrafted Jaipur Blue Pottery Floral Motif Vase",
    transcript: "Traditional Jaipur blue pottery decorative vase made from quartz stone powder without clay taking 5 hours.",
    material: 200,
    hours: 5,
    margin: 20,
    intended: 815,
    gi_number: "GI-RJ-003"
  },
  dhokra: {
    artisan: "Gurucharan Mohapatra",
    state: "Odisha",
    image: "/static/images/product_31.svg",
    category: "Metallurgy & Sculpture",
    title: "Tribal Dhokra Lost-Wax Bell Metal Dancing Figurine",
    transcript: "Prehistoric lost-wax cast bell metal brass tribal dancing figurine crafted using 4000 year ancient metallurgy taking 18 hours.",
    material: 600,
    hours: 18,
    margin: 25,
    intended: 2425,
    gi_number: "GI-OD-004"
  },
  kanchipuram: {
    artisan: "Kalyanasundaram Swamy",
    state: "Tamil Nadu",
    image: "/static/images/product_41.svg",
    category: "Handloom & Silk",
    title: "Pure Zari Handwoven Kanchipuram Temple Border Silk Saree",
    transcript: "Pure mulberry silk with authentic Korvai temple border and pure silver electroplated zari woven over 22 hours.",
    material: 1200,
    hours: 22,
    margin: 25,
    intended: 3800,
    gi_number: "GI-TN-005"
  },
  bamboo: {
    artisan: "Debabrata Saikia",
    state: "Assam",
    image: "/static/images/product_51.svg",
    category: "Sustainable Crafts",
    title: "Artisanal Hand-Braided Organic Bamboo Storage Basket",
    transcript: "100% Eco-friendly matured split organic bamboo basket with spiral lattice weave crafted over 6 hours.",
    material: 150,
    hours: 6,
    margin: 20,
    intended: 750,
    gi_number: "AS-CRAFT-006"
  },
  kantha: {
    artisan: "Moumita Banerjee",
    state: "West Bengal",
    image: "/static/images/product_61.svg",
    category: "Handloom & Textiles",
    title: "Santiniketan Handcrafted Kantha Embroidered Silk Dupatta",
    transcript: "Pure Tussar silk dupatta featuring folkloric village life embroidered in thousands of running stitches taking 16 hours.",
    material: 500,
    hours: 16,
    margin: 25,
    intended: 1950,
    gi_number: "GI-WB-006"
  },
  pashmina: {
    artisan: "Ghulam Mohammad Mir",
    state: "Jammu & Kashmir",
    image: "/static/images/product_71.svg",
    category: "Luxury Handloom",
    title: "Royal Handspun Kashmiri Pashmina Cashmere Shawl",
    transcript: "Pure 100% Changthangi goat cashmere woven on traditional wooden handloom with delicate sozni needlework over 24 hours.",
    material: 2000,
    hours: 24,
    margin: 30,
    intended: 5600,
    gi_number: "GI-JK-007"
  }
};

// 1. Navigation Controller & Role Access Enforcement
function updateRoleAccess(role) {
  const studioBtn = document.getElementById('nav-btn-studio');
  const adminBtn = document.getElementById('nav-btn-admin');
  const heroBtn = document.getElementById('heroBtnPrimary');

  if (role === 'BUYER') {
    if (studioBtn) studioBtn.style.display = 'none';
    if (adminBtn) adminBtn.style.display = 'none';
    if (heroBtn) heroBtn.innerText = "🛍️ Explore Handcrafted Products";
  } else if (role === 'ARTISAN') {
    if (studioBtn) studioBtn.style.display = 'flex';
    if (adminBtn) adminBtn.style.display = 'none';
    if (heroBtn) heroBtn.innerText = "🎙️ Open Artisan Voice Studio";
  } else if (role === 'ADMIN') {
    if (studioBtn) studioBtn.style.display = 'none';
    if (adminBtn) adminBtn.style.display = 'flex';
    if (heroBtn) heroBtn.innerText = "🏛️ Open Admin Control Center";
  }
}

function handleHeroPrimaryAction() {
  if (currentUser.role === 'ARTISAN') {
    navigateTo('view-studio');
  } else if (currentUser.role === 'ADMIN') {
    navigateTo('view-admin');
  } else {
    navigateTo('view-marketplace');
  }
}

function navigateTo(viewId) {
  // Role Access Guard
  if (viewId === 'view-studio' && currentUser.role !== 'ARTISAN') {
    showToast("🔒 Artisan Studio is reserved exclusively for artisans. Switch persona in top bar.", "warning", 3000);
    navigateTo('view-marketplace');
    return;
  }

  if (viewId === 'view-admin' && currentUser.role !== 'ADMIN') {
    showToast("🔒 Admin Portal is restricted to authorized SIH Admin persona.", "warning", 3000);
    navigateTo('view-marketplace');
    return;
  }

  document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));

  const targetView = document.getElementById(viewId);
  if (targetView) targetView.classList.add('active');

  const navKey = viewId.replace('view-', '');
  const navBtn = document.getElementById(`nav-btn-${navKey}`);
  if (navBtn) navBtn.classList.add('active');

  if (viewId === 'view-home') loadFeaturedProducts();
  if (viewId === 'view-marketplace') loadMarketplaceProducts();
  if (viewId === 'view-makers') loadArtisansList();
  if (viewId === 'view-orders') loadOrdersList();
  if (viewId === 'view-admin') loadAdminDashboard();
  if (viewId === 'view-impact') loadPublicImpactData();

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 2. Persona Switcher & Management
async function switchDemoUser(identifier) {
  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: 'ARTISAN', identifier: identifier })
    });
    const data = await res.json();
    if (data.authenticated) {
      currentUser = data.user;
      currentUser.role = data.role;
      const roleIcon = data.role === 'ARTISAN' ? '👩‍🎨' : (data.role === 'BUYER' ? '🛍️' : '🏛️');
      
      document.getElementById('userRoleIcon').innerText = roleIcon;
      document.getElementById('currentUserName').innerText = `${data.user.name} (${data.role})`;
      document.getElementById('filterPersonaName').innerText = data.user.name;

      const dropdown = document.getElementById('personaQuickDropdown');
      if (dropdown && dropdown.value !== identifier) {
        dropdown.value = identifier;
      }

      closeModal('personaModal');
      updateRoleAccess(data.role);

      // Route according to role
      if (data.role === 'ARTISAN') {
        document.getElementById('studioArtisanName').value = data.user.name;
        if (data.user.state) document.getElementById('studioStateSelect').value = data.user.state;
        navigateTo('view-studio');
      } else if (data.role === 'BUYER') {
        navigateTo('view-marketplace');
      } else {
        navigateTo('view-admin');
      }
    }
  } catch (e) {
    console.error("Persona switch error:", e);
  }
}

async function openPersonaModal() {
  try {
    const res = await fetch('/api/auth/demo-personas');
    const data = await res.json();
    const personas = data.data;

    const artisans = personas.filter(p => p.role === 'ARTISAN');
    const buyers = personas.filter(p => p.role === 'BUYER');
    const admin = personas.filter(p => p.role === 'ADMIN');

    document.getElementById('personaArtisansGrid').innerHTML = artisans.map(a => `
      <div class="persona-select-card ${currentUser.name === a.name ? 'active' : ''}" onclick="switchDemoUser('${a.identifier}')">
        <img src="${a.avatar || 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400'}" alt="${a.name}">
        <div>
          <div style="font-weight: 700; font-size: 0.9rem;">${a.name}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${a.craft} • ${a.state}</div>
          <span style="font-size: 0.7rem; background: var(--success-light); color: var(--success); padding: 1px 6px; border-radius: 4px; font-weight: bold;">Verified Artisan</span>
        </div>
      </div>
    `).join('');

    document.getElementById('personaBuyersGrid').innerHTML = buyers.map(b => `
      <div class="persona-select-card ${currentUser.name === b.name ? 'active' : ''}" onclick="switchDemoUser('${b.identifier}')">
        <img src="${b.avatar || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400'}" alt="${b.name}">
        <div>
          <div style="font-weight: 700; font-size: 0.9rem;">${b.name}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${b.district}, ${b.state}</div>
          <span style="font-size: 0.7rem; background: #e0f2fe; color: #0284c7; padding: 1px 6px; border-radius: 4px; font-weight: bold;">Verified Buyer</span>
        </div>
      </div>
    `).join('');

    document.getElementById('personaAdminGrid').innerHTML = admin.map(ad => `
      <div class="persona-select-card ${currentUser.name === ad.name ? 'active' : ''}" onclick="switchDemoUser('${ad.identifier}')">
        <img src="${ad.avatar || 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400'}" alt="${ad.name}">
        <div>
          <div style="font-weight: 700; font-size: 0.9rem;">${ad.name}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${ad.designation}</div>
          <span style="font-size: 0.7rem; background: #fef3c7; color: #b45309; padding: 1px 6px; border-radius: 4px; font-weight: bold;">Ecosystem Admin</span>
        </div>
      </div>
    `).join('');

    document.getElementById('personaModal').classList.add('active');
  } catch (e) {
    console.error(e);
  }
}

// 3. Drag & Drop and Image Upload Controller
function initDragAndDrop() {
  const dropZone = document.getElementById('dropZone');
  if (!dropZone) return;

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.add('dragover');
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.remove('dragover');
    }, false);
  });

  dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
      handleImageFile(files[0]);
    }
  });
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    handleImageFile(file);
  }
}

function handleImageFile(file) {
  const reader = new FileReader();
  reader.onload = function(e) {
    const base64Data = e.target.result;
    processUploadedImage(base64Data);
  };
  reader.readAsDataURL(file);
}

async function processUploadedImage(imageUrlOrBase64) {
  currentUploadedImageUrl = imageUrlOrBase64;
  
  // Show Preview Box
  const previewBox = document.getElementById('imagePreviewContainer');
  const previewImg = document.getElementById('imagePreviewImg');
  const dropZone = document.getElementById('dropZone');
  const aiBox = document.getElementById('aiVisionResultBox');
  const aiText = document.getElementById('aiVisionResultText');

  previewImg.src = imageUrlOrBase64;
  previewBox.style.display = 'block';
  dropZone.style.display = 'none';

  // Run instant AI Computer Vision Inspection
  try {
    const craftHint = document.getElementById('studioArtisanName').value;
    const res = await fetch('/api/upload-image', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_data: imageUrlOrBase64, craft_hint: craftHint })
    });
    const data = await res.json();
    const ai = data.ai_analysis;

    aiText.innerHTML = `<b>${ai.craft_detected}</b> • Motifs: ${ai.motifs_detected.join(', ')} • <b>${Math.round(ai.confidence_score*100)}% Authenticity Confidence</b>`;
    aiBox.style.display = 'block';
  } catch (e) {
    console.error("Image AI error:", e);
  }
}

function removeUploadedImage() {
  currentUploadedImageUrl = null;
  document.getElementById('imagePreviewContainer').style.display = 'none';
  document.getElementById('dropZone').style.display = 'block';
  document.getElementById('aiVisionResultBox').style.display = 'none';
  document.getElementById('fileInput').value = '';
}

// 4. Web Speech API Initialization
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('voiceTranscriptInput').value = transcript;
    toggleVoiceRecording(false);
    runCompleteAIPipeline();
  };

  recognition.onerror = () => {
    toggleVoiceRecording(false);
  };
}

function toggleVoiceRecording(forceState) {
  const micContainer = document.getElementById('voiceMicContainer');
  const micStatus = document.getElementById('micStatusText');

  isRecording = forceState !== undefined ? forceState : !isRecording;

  if (isRecording && recognition) {
    try {
      recognition.lang = 'mr-IN'; // Default Indic dialect
      recognition.start();
      micContainer.classList.add('recording');
      micStatus.innerText = "Listening to speech dialect... (Bhashini AI)";
    } catch (e) {
      console.log("Speech recognition error:", e);
    }
  } else {
    if (recognition) recognition.stop();
    micContainer.classList.remove('recording');
    micStatus.innerText = "Tap to Speak (Bhashini AI)";
  }
}

// 5. Preset Loader
function loadPreset(key) {
  const data = CRAFT_PRESETS[key];
  if (!data) return;

  document.querySelectorAll('.chip-btn').forEach(b => b.classList.remove('active'));
  if (event && event.target && event.target.classList) {
    event.target.classList.add('active');
  }

  document.getElementById('studioArtisanName').value = data.artisan;
  document.getElementById('studioStateSelect').value = data.state;
  document.getElementById('voiceTranscriptInput').value = data.transcript;
  document.getElementById('studioMaterialCost').value = data.material;
  document.getElementById('studioLaborHours').value = data.hours;
  document.getElementById('studioIntendedPrice').value = data.intended;
  document.getElementById('studioMarginPct').value = data.margin;

  processUploadedImage(data.image);
  runCompleteAIPipeline();
}

// 6. Complete Multimodal AI Pipeline
async function runCompleteAIPipeline() {
  const transcript = document.getElementById('voiceTranscriptInput').value;
  const artisanName = document.getElementById('studioArtisanName').value;
  const state = document.getElementById('studioStateSelect').value;

  try {
    const nlpRes = await fetch('/api/analyze-craft', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ voice_transcript: transcript, artisan_name: artisanName, artisan_region: state })
    });
    const nlpData = await nlpRes.json();
    currentExtractedData = nlpData.data;

    document.getElementById('studioHeritageStory').value = currentExtractedData.heritage_story;
    document.getElementById('giStatusText').innerText = `${currentExtractedData.gi_number || 'GI-VERIFIED'} • VERIFIED AUTHENTIC`;

    runPriceCalculation();
  } catch (e) {
    console.error("AI pipeline error:", e);
  }
}

// 7. Transparent Fair Price Calculation
async function runPriceCalculation() {
  const material = parseFloat(document.getElementById('studioMaterialCost').value) || 0;
  const hours = parseFloat(document.getElementById('studioLaborHours').value) || 0;
  const intended = parseFloat(document.getElementById('studioIntendedPrice').value) || 0;
  const margin = parseFloat(document.getElementById('studioMarginPct').value) || 20;
  const state = document.getElementById('studioStateSelect').value;

  try {
    const res = await fetch('/api/calculate-price', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        material_cost: material,
        labor_hours: hours,
        state_name: state,
        desired_margin_pct: margin,
        artisan_intended_price: intended
      })
    });
    const priceRes = await res.json();
    currentPricingData = priceRes.data;

    document.getElementById('lblBreakdownMaterial').innerText = `₹${currentPricingData.raw_material.toFixed(2)}`;
    document.getElementById('lblBreakdownLabor').innerText = `₹${currentPricingData.artisan_labor_wage.toFixed(2)} (${hours} hrs @ ₹${currentPricingData.hourly_wage_rate}/hr)`;
    document.getElementById('lblBreakdownOverhead').innerText = `₹${(currentPricingData.overheads + currentPricingData.packaging).toFixed(2)}`;
    document.getElementById('lblBreakdownLogistics').innerText = `₹${currentPricingData.logistics.toFixed(2)}`;
    document.getElementById('lblBreakdownMargin').innerText = `₹${currentPricingData.artisan_margin.toFixed(2)}`;
    document.getElementById('lblBreakdownTotal').innerText = `₹${currentPricingData.fair_selling_price.toLocaleString('en-IN')}.00`;

    const alertBox = document.getElementById('underpricingAlertContainer');
    if (currentPricingData.underpricing_warning) {
      alertBox.innerHTML = `
        <div class="alert-box alert-warning">
          <div>${currentPricingData.advisory_message}</div>
        </div>
      `;
    } else {
      alertBox.innerHTML = `
        <div class="alert-box alert-success">
          <div>${currentPricingData.advisory_message || '✅ Fair wage statutory living baseline protected.'}</div>
        </div>
      `;
    }
  } catch (e) {
    console.error("Price calc error:", e);
  }
}

// 8. Publish Listing to Marketplace
async function publishStudioListing() {
  if (!currentExtractedData || !currentPricingData) {
    await runCompleteAIPipeline();
  }

  const payload = {
    artisan_name: document.getElementById('studioArtisanName').value,
    title: currentExtractedData.detected_craft_title,
    short_description: currentExtractedData.detected_craft_title,
    description: currentExtractedData.heritage_story,
    heritage_story: currentExtractedData.heritage_story,
    category: currentExtractedData.category,
    craft_type: currentExtractedData.craft_type,
    state_cluster: document.getElementById('studioStateSelect').value,
    materials: currentExtractedData.materials,
    technique: currentExtractedData.technique,
    motifs: currentExtractedData.motifs,
    dimensions: currentExtractedData.dimensions,
    weight: currentExtractedData.weight,
    care_instructions: currentExtractedData.care_instructions,
    image_urls: [currentUploadedImageUrl || CRAFT_PRESETS.paithani.image],
    material_cost: currentPricingData.raw_material,
    labor_hours: currentPricingData.labor_hours,
    hourly_wage_rate: currentPricingData.hourly_wage_rate,
    suggested_fair_price: currentPricingData.fair_selling_price,
    selling_price: currentPricingData.fair_selling_price,
    gi_number: currentExtractedData.gi_number,
    gi_verified: true,
    tags: currentExtractedData.tags,
    status: "PUBLISHED"
  };

  try {
    const res = await fetch('/api/products', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      showToast("🎉 Product published to open marketplace & ONDC Beckn catalog!", "success", 2500);
      navigateTo('view-marketplace');
    }
  } catch (e) {
    console.error("Publish error:", e);
  }
}

// 9. Offline Draft Saving
function saveDraftOffline() {
  const draft = {
    artisan_name: document.getElementById('studioArtisanName').value,
    title: currentExtractedData?.detected_craft_title || "Handcrafted Heritage Item",
    heritage_story: document.getElementById('studioHeritageStory').value,
    category: "Handicrafts",
    craft_type: "Handmade",
    state_cluster: document.getElementById('studioStateSelect').value,
    material_cost: parseFloat(document.getElementById('studioMaterialCost').value) || 0,
    labor_hours: parseFloat(document.getElementById('studioLaborHours').value) || 0,
    hourly_wage_rate: 65.0,
    suggested_fair_price: currentPricingData?.fair_selling_price || 2344.0,
    selling_price: currentPricingData?.fair_selling_price || 2344.0,
    image_urls: [currentUploadedImageUrl || CRAFT_PRESETS.paithani.image]
  };

  OfflineDraftManager.saveDraft(draft);
  showToast("💾 Draft saved locally in offline storage!", "info", 2000);
}

// 10. Marketplace Products Loader
async function loadMarketplaceProducts(query = "") {
  const url = query ? `/api/products?search=${encodeURIComponent(query)}` : '/api/products';
  try {
    const res = await fetch(url);
    const data = await res.json();
    renderProductCards(data.data, 'marketplaceProductsGrid');
  } catch (e) {
    console.error("Fetch products error:", e);
  }
}

async function loadFeaturedProducts() {
  try {
    const res = await fetch('/api/products');
    const data = await res.json();
    renderProductCards(data.data.slice(0, 4), 'homeFeaturedProducts');
  } catch (e) {
    console.error("Fetch featured products error:", e);
  }
}

function renderProductCards(products, targetElementId) {
  const container = document.getElementById(targetElementId);
  if (!container) return;

  if (products.length === 0) {
    container.innerHTML = `<div style="grid-column: 1/-1; padding: 32px; text-align: center; color: var(--text-muted);">No handcrafted items match the filter criteria.</div>`;
    return;
  }

  container.innerHTML = products.map(p => {
    const inWishlist = currentWishlist.includes(p.id);
    return `
      <div class="product-card">
        <div class="product-img-wrapper" onclick="openProductDetailModal(${p.id})">
          <img src="${p.image_urls[0] || '/static/images/product_' + p.id + '.svg'}" alt="${p.title}" loading="lazy" onerror="this.onerror=null; this.src='/static/images/product_${p.id}.svg';">
          ${p.gi_verified ? '<span class="gi-tag-pill">🛡️ GI Protected</span>' : ''}
          <button class="wishlist-btn-overlay wishlist-btn-${p.id} ${inWishlist ? 'active' : ''}" onclick="toggleWishlist(${p.id}, event)" title="${inWishlist ? 'Remove from Wishlist' : 'Add to Wishlist'}">
            ${inWishlist ? '❤️' : '🤍'}
          </button>
        </div>
        <div class="product-info">
          <div class="product-category">${p.category}</div>
          <div class="product-title" onclick="openProductDetailModal(${p.id})" style="cursor: pointer;">${p.title}</div>
          <div class="product-artisan">by <b>${p.artisan_name}</b> • ${p.state_cluster}</div>
          <div class="price-row">
            <div>
              <div class="price-val">₹${p.selling_price.toLocaleString('en-IN')}</div>
              <div class="wage-component-badge">⚖️ Protected Wage: ₹${(p.labor_hours * p.hourly_wage_rate).toFixed(0)}</div>
            </div>
            <button class="btn-primary" style="padding: 6px 12px; font-size: 0.82rem;" onclick="addToCart(${p.id})">🛒 Add</button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// 11. Wishlist Functions
function toggleWishlist(productId, event) {
  if (event) event.stopPropagation();
  const idx = currentWishlist.indexOf(productId);
  if (idx > -1) {
    currentWishlist.splice(idx, 1);
    showToast('Item removed from Wishlist', 'info', 2000);
  } else {
    currentWishlist.push(productId);
    showToast('❤️ Added to your Wishlist!', 'success', 2000);
  }
  localStorage.setItem('artisan_wishlist', JSON.stringify(currentWishlist));
  updateWishlistBadge();

  // Refresh visual state of hearts
  document.querySelectorAll(`.wishlist-btn-${productId}`).forEach(btn => {
    if (currentWishlist.includes(productId)) {
      btn.classList.add('active');
      btn.innerHTML = '❤️';
    } else {
      btn.classList.remove('active');
      btn.innerHTML = '🤍';
    }
  });

  if (document.getElementById('wishlistModal').classList.contains('active')) {
    renderWishlistItems();
  }
}

async function openWishlistModal() {
  renderWishlistItems();
  document.getElementById('wishlistModal').classList.add('active');
}

async function renderWishlistItems() {
  const container = document.getElementById('wishlistItemsContainer');
  if (!container) return;

  if (currentWishlist.length === 0) {
    container.innerHTML = `
      <div style="padding: 36px 16px; text-align: center; color: var(--text-muted);">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">🤍</div>
        <div style="font-weight: 700; font-size: 1.05rem; color: #334155;">Your Wishlist is currently empty</div>
        <p style="font-size: 0.85rem; margin-top: 4px; max-width: 320px; margin: 4px auto 14px;">Tap the heart icon on any handcrafted product in the marketplace to save it here.</p>
        <button class="btn-primary" style="margin: 0 auto;" onclick="closeModal('wishlistModal'); navigateTo('view-marketplace');">Explore Marketplace →</button>
      </div>
    `;
    return;
  }

  try {
    const res = await fetch('/api/products');
    const data = await res.json();
    const items = data.data.filter(p => currentWishlist.includes(p.id));

    container.innerHTML = items.map(p => `
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--border-color); gap: 12px; flex-wrap: wrap;">
        <div style="display: flex; gap: 12px; align-items: center; flex: 1; min-width: 240px;">
          <img src="${p.image_urls[0] || '/static/images/product_' + p.id + '.svg'}" style="width: 54px; height: 54px; border-radius: 6px; object-fit: cover;" onerror="this.onerror=null; this.src='/static/images/product_${p.id}.svg';">
          <div>
            <div style="font-weight: 700; font-size: 0.92rem; line-height: 1.3;">${p.title}</div>
            <div style="font-size: 0.78rem; color: var(--text-muted);">by <b>${p.artisan_name}</b> • ${p.state_cluster}</div>
            <div style="font-weight: 800; color: var(--primary); font-size: 0.95rem; margin-top: 2px;">₹${p.selling_price.toLocaleString('en-IN')}</div>
          </div>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
          <button class="btn-primary" style="padding: 6px 12px; font-size: 0.8rem;" onclick="addToCart(${p.id})">🛒 Add to Cart</button>
          <button class="btn-secondary" style="padding: 6px 10px; font-size: 0.8rem; color: var(--danger);" onclick="toggleWishlist(${p.id})" title="Remove">✕</button>
        </div>
      </div>
    `).join('');
  } catch (e) {
    console.error(e);
  }
}

// 12. Product Detail Modal
async function openProductDetailModal(productId) {
  try {
    const res = await fetch(`/api/products/${productId}`);
    const data = await res.json();
    const p = data.data;
    const inWishlist = currentWishlist.includes(p.id);

    const modalBody = document.getElementById('productDetailBody');
    modalBody.innerHTML = `
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;">
        <div>
          <div style="position: relative;">
            <img src="${p.image_urls[0]}" onerror="this.onerror=null; this.src='/static/images/product_${p.id}.svg';" style="width: 100%; border-radius: var(--radius-md); box-shadow: var(--shadow-sm);" alt="${p.title}">
            <button class="wishlist-btn-overlay wishlist-btn-${p.id} ${inWishlist ? 'active' : ''}" onclick="toggleWishlist(${p.id}, event)" style="top: 12px; right: 12px;">
              ${inWishlist ? '❤️' : '🤍'}
            </button>
          </div>
          <div style="margin-top: 12px; background: #f0fdf4; border: 1px solid #bbf7d0; padding: 10px; border-radius: var(--radius-sm); font-size: 0.82rem;">
            <b>🛡️ GI Certificate:</b> ${p.gi_number || 'GI-MH-001'} (Verified National Registry Entry)
          </div>
        </div>
        <div>
          <div style="font-size: 0.8rem; text-transform: uppercase; color: var(--primary); font-weight: bold;">${p.category}</div>
          <h2 style="font-family: var(--font-serif); margin: 6px 0 10px;">${p.title}</h2>
          <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 12px;">Crafted by <b>${p.artisan_name}</b> in ${p.state_cluster}</div>

          <p style="font-size: 0.92rem; line-height: 1.6; margin-bottom: 14px;">${p.heritage_story || p.description}</p>

          <div style="background: #f8fafc; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 12px; margin-bottom: 14px; font-size: 0.85rem;">
            <div><b>Materials:</b> ${p.materials.join(', ') || 'Natural organic fibers'}</div>
            <div><b>Dimensions:</b> ${p.dimensions || 'Standard'} • <b>Weight:</b> ${p.weight || '500g'}</div>
            <div><b>Care:</b> ${p.care_instructions || 'Dry clean only'}</div>
          </div>

          <div class="price-row" style="margin-bottom: 16px;">
            <div>
              <div class="price-val" style="font-size: 1.5rem;">₹${p.selling_price.toLocaleString('en-IN')}</div>
              <div style="font-size: 0.78rem; color: var(--success); font-weight: 600;">⚖️ ₹${(p.labor_hours * p.hourly_wage_rate).toFixed(0)} Direct Living Wage in Escrow</div>
            </div>
            <div style="display: flex; gap: 8px;">
              <button class="btn-secondary" onclick="addToCart(${p.id})">🛒 Add to Cart</button>
              <button class="btn-primary" onclick="buyNowSingle(${p.id})">🔒 Buy with Escrow</button>
            </div>
          </div>
        </div>
      </div>
    `;

    document.getElementById('productDetailModal').classList.add('active');
  } catch (e) {
    console.error("Detail modal error:", e);
  }
}

// 13. Meet the Makers / Artisans List
async function loadArtisansList() {
  try {
    const res = await fetch('/api/artisans');
    const data = await res.json();
    const container = document.getElementById('artisansListGrid');
    container.innerHTML = data.data.map(art => `
      <div class="product-card" style="padding: 20px;">
        <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 14px;">
          <img src="${art.profile_photo || 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400'}" style="width: 64px; height: 64px; border-radius: 50%; object-fit: cover; border: 2px solid var(--primary);">
          <div>
            <h3 style="font-size: 1.1rem;">${art.name}</h3>
            <div style="font-size: 0.8rem; color: var(--text-muted);">${art.state_cluster} • ${art.years_experience} yrs exp</div>
            <span class="gi-tag-pill" style="position: static; display: inline-flex; margin-top: 4px;">✓ ${art.verification_status}</span>
          </div>
        </div>
        <p style="font-size: 0.85rem; color: #475569; margin-bottom: 12px; flex: 1;">${art.story}</p>
        <div style="font-size: 0.78rem; background: #f8fafc; padding: 8px 12px; border-radius: var(--radius-sm); margin-bottom: 12px;">
          <div><b>Guild:</b> ${art.gi_association || 'Registered Handloom Union'}</div>
          <div><b>Verified Orders:</b> ${art.verified_orders_count} orders completed</div>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn-secondary" style="flex: 1; justify-content: center; font-size: 0.8rem;" onclick="filterMarketplaceByArtisan(${art.id})">Catalog →</button>
          <button class="btn-primary" style="flex: 1; justify-content: center; font-size: 0.8rem;" onclick="switchDemoUser('DEMO-ARTISAN-00${art.id}')">Switch Persona</button>
        </div>
      </div>
    `).join('');
  } catch (e) {
    console.error("Artisans error:", e);
  }
}

function filterMarketplaceByArtisan(artisanId) {
  navigateTo('view-marketplace');
  fetch(`/api/products?artisan_id=${artisanId}`)
    .then(r => r.json())
    .then(data => renderProductCards(data.data, 'marketplaceProductsGrid'));
}

// 14. Cart & Quantity Management
async function normalizeCart() {
  if (!Array.isArray(currentCart)) {
    currentCart = [];
    saveCart();
    return;
  }
  let needsSave = false;
  let productsCache = null;

  for (let i = 0; i < currentCart.length; i++) {
    const it = currentCart[i];
    if (typeof it === 'number' || !it || !it.title || typeof it.price !== 'number' || isNaN(it.price)) {
      const prodId = typeof it === 'number' ? it : (it ? it.id : 1);
      try {
        if (!productsCache) {
          const res = await fetch('/api/products');
          productsCache = (await res.json()).data;
        }
        const found = productsCache.find(p => p.id === prodId);
        if (found) {
          currentCart[i] = {
            id: found.id,
            title: found.title,
            price: found.selling_price,
            image: found.image_urls[0] || `/static/images/product_${found.id}.svg`,
            labor_hours: found.labor_hours || 12,
            hourly_wage_rate: found.hourly_wage_rate || 65,
            artisan_name: found.artisan_name,
            quantity: typeof it === 'object' && it && it.quantity ? it.quantity : 1
          };
          needsSave = true;
        }
      } catch (err) {
        console.error("Cart normalization error:", err);
      }
    }
  }
  if (needsSave) {
    saveCart();
  }
}

async function addToCart(productId) {
  try {
    const res = await fetch(`/api/products/${productId}`);
    const data = await res.json();
    const prod = data.data;

    await normalizeCart();
    const existing = currentCart.find(it => it.id === productId);
    if (existing) {
      existing.quantity = (existing.quantity || 1) + 1;
    } else {
      currentCart.push({
        id: prod.id,
        title: prod.title,
        price: prod.selling_price,
        image: prod.image_urls[0] || `/static/images/product_${prod.id}.svg`,
        labor_hours: prod.labor_hours || 12,
        hourly_wage_rate: prod.hourly_wage_rate || 65,
        artisan_name: prod.artisan_name,
        quantity: 1
      });
    }
    saveCart();
    showToast(`🛒 "${prod.title.slice(0, 24)}..." added to cart!`, 'success', 2000);

    if (document.getElementById('cartModal').classList.contains('active')) {
      renderCartItems();
    }
  } catch (e) {
    console.error(e);
  }
}

function updateCartQuantity(productId, delta) {
  const item = currentCart.find(it => it.id === productId);
  if (!item) return;

  item.quantity = (item.quantity || 1) + delta;
  if (item.quantity <= 0) {
    currentCart = currentCart.filter(it => it.id !== productId);
    showToast('Item removed from cart', 'info', 2000);
  }
  saveCart();
  renderCartItems();
}

function removeFromCart(productId) {
  currentCart = currentCart.filter(it => it.id !== productId);
  saveCart();
  renderCartItems();
  showToast('Item removed from cart', 'info', 2000);
}

async function renderCartItems() {
  await normalizeCart();
  const container = document.getElementById('cartItemsContainer');
  const breakdownBox = document.getElementById('cartFinancialBreakdown');
  const payBtn = document.getElementById('btnProceedToPayment');
  if (!container) return;

  if (currentCart.length === 0) {
    container.innerHTML = `
      <div style="padding: 36px 16px; text-align: center; color: var(--text-muted);">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">🛒</div>
        <div style="font-weight: 700; font-size: 1.05rem; color: #334155;">Your fair-trade cart is empty</div>
        <p style="font-size: 0.85rem; margin-top: 4px; max-width: 320px; margin: 4px auto 14px;">Explore authentic handloom creations crafted by verified master artisans.</p>
        <button class="btn-primary" style="margin: 0 auto;" onclick="closeModal('cartModal'); navigateTo('view-marketplace');">Explore Marketplace →</button>
      </div>
    `;
    if (breakdownBox) breakdownBox.innerHTML = '';
    if (payBtn) payBtn.style.display = 'none';
    return;
  }

  if (payBtn) payBtn.style.display = 'block';

  let subtotal = 0;
  let totalWageProtected = 0;

  container.innerHTML = currentCart.map(it => {
    const qty = it.quantity || 1;
    const price = typeof it.price === 'number' ? it.price : 0;
    const hours = it.labor_hours || 10;
    const wageRate = it.hourly_wage_rate || 65;
    const itemSubtotal = price * qty;
    const itemWage = (hours * wageRate) * qty;
    subtotal += itemSubtotal;
    totalWageProtected += itemWage;

    return `
      <div class="cart-item-row">
        <img src="${it.image}" class="cart-item-img" onerror="this.onerror=null; this.src='/static/images/product_${it.id}.svg';">
        <div>
          <div style="font-weight: 700; font-size: 0.92rem; line-height: 1.3;">${it.title}</div>
          <div style="font-size: 0.78rem; color: var(--text-muted);">by <b>${it.artisan_name || 'Master Artisan'}</b></div>
          <div style="font-size: 0.75rem; color: var(--success); font-weight: 600; margin-top: 3px;">⚖️ Protected Wage: ₹${itemWage.toFixed(0)}</div>
        </div>
        <div class="cart-qty-controls">
          <button class="cart-qty-btn" onclick="updateCartQuantity(${it.id}, -1)">−</button>
          <span class="cart-qty-val">${qty}</span>
          <button class="cart-qty-btn" onclick="updateCartQuantity(${it.id}, 1)">+</button>
        </div>
        <div style="text-align: right;">
          <div style="font-weight: 800; font-size: 1.05rem;">₹${itemSubtotal.toLocaleString('en-IN')}</div>
          <button style="background: none; border: none; color: var(--danger); font-size: 0.78rem; cursor: pointer; padding: 2px 0;" onclick="removeFromCart(${it.id})">🗑️ Remove</button>
        </div>
      </div>
    `;
  }).join('');

  const deliveryFee = subtotal >= 2500 ? 0 : 100;
  const totalAmount = subtotal + deliveryFee;
  const middlemanSaved = Math.round(subtotal * 0.45);

  if (breakdownBox) {
    breakdownBox.innerHTML = `
      <div class="cart-breakdown-card">
        <div class="cart-savings-banner">
          <span>🎉</span>
          <span><b>₹${middlemanSaved.toLocaleString('en-IN')} saved</b> by bypassing traditional middlemen markups!</span>
        </div>
        <div class="breakdown-row">
          <span>Items Subtotal (${currentCart.reduce((sum, it) => sum + (it.quantity || 1), 0)} items)</span>
          <span style="font-weight: 600;">₹${subtotal.toLocaleString('en-IN')}</span>
        </div>
        <div class="breakdown-row" style="color: var(--success); font-weight: 600;">
          <span>⚖️ Direct Artisan Living Wage Included</span>
          <span>₹${totalWageProtected.toLocaleString('en-IN')}</span>
        </div>
        <div class="breakdown-row">
          <span>🚚 ONDC SpeedPost Logistics Delivery</span>
          <span>${deliveryFee === 0 ? '<span style="color: var(--success); font-weight: 700;">FREE (Orders > ₹2,500)</span>' : '₹100'}</span>
        </div>
        <div class="breakdown-row">
          <span>🛡️ Platform Escrow & Verification Fee</span>
          <span style="color: var(--success); font-weight: 600;">₹0.00 (0% Zero Commission)</span>
        </div>
        <div class="breakdown-row total-row">
          <span>Total Amount Payable</span>
          <span style="color: var(--primary);">₹${totalAmount.toLocaleString('en-IN')}</span>
        </div>
      </div>
    `;
  }
}

async function openCartModal() {
  await renderCartItems();
  document.getElementById('cartModal').classList.add('active');
}

async function buyNowSingle(productId) {
  closeModal('productDetailModal');
  try {
    const res = await fetch(`/api/products/${productId}`);
    const data = await res.json();
    const prod = data.data;

    currentCart = [{
      id: prod.id,
      title: prod.title,
      price: prod.selling_price,
      image: prod.image_urls[0] || `/static/images/product_${prod.id}.svg`,
      labor_hours: prod.labor_hours || 12,
      hourly_wage_rate: prod.hourly_wage_rate || 65,
      artisan_name: prod.artisan_name,
      quantity: 1
    }];
    saveCart();
    openCartModal();
  } catch (e) {
    console.error(e);
  }
}

async function checkDeliveryPincode() {
  const pin = document.getElementById('checkoutPincodeInput').value;
  try {
    const res = await fetch('/api/logistics/check-pincode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pincode: pin })
    });
    const data = await res.json();
    const msg = document.getElementById('pincodeStatusMsg');
    if (data.data.serviceable) {
      msg.innerHTML = `<span style="color: var(--success); font-weight: 600;">✓ Serviceable via SpeedPost. Estimated delivery: ${data.data.estimated_delivery_date}</span>`;
      showToast("✓ PIN code serviceable via SpeedPost!", "success", 2000);
    } else {
      msg.innerHTML = `<span style="color: var(--danger); font-weight: 600;">⚠️ ${data.data.message}</span>`;
      showToast(data.data.message, "warning", 2000);
    }
  } catch (e) {
    console.error(e);
  }
}

// 15. Demo Payment Portal Management
let currentPaymentTab = 'upi';

function switchPaymentTab(tabName) {
  currentPaymentTab = tabName;
  ['upi', 'card', 'net'].forEach(t => {
    const btn = document.getElementById(`payTabBtn${t.charAt(0).toUpperCase() + t.slice(1)}`);
    const content = document.getElementById(`payTabContent${t.charAt(0).toUpperCase() + t.slice(1)}`);
    if (btn) btn.classList.toggle('active', t === tabName);
    if (content) content.style.display = t === tabName ? 'block' : 'none';
  });
}

async function openDemoPaymentPortal() {
  await normalizeCart();
  if (currentCart.length === 0) {
    showToast("Your cart is empty.", "warning", 2000);
    return;
  }
  const subtotal = currentCart.reduce((sum, it) => sum + ((it.price || 0) * (it.quantity || 1)), 0);
  const delivery = subtotal >= 2500 ? 0 : 100;
  const total = subtotal + delivery;

  document.getElementById('paymentPortalTotalVal').innerText = `₹${total.toLocaleString('en-IN')}`;
  
  const holderInput = document.getElementById('demoCardHolderName');
  if (holderInput) holderInput.value = document.getElementById('checkoutBuyerName').value || currentUser.name;

  closeModal('cartModal');
  switchPaymentTab('upi');
  document.getElementById('demoPaymentModal').classList.add('active');
}

async function simulateAuthorizeEscrowPayment() {
  const btn = document.getElementById('btnSimulatePayment');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner-border" style="display:inline-block; width:16px; height:16px; border:2px solid #fff; border-top-color:transparent; border-radius:50%; animation: spin 0.8s linear infinite; margin-right:8px;"></span> 🔒 Securing Escrow & Routing via ONDC...`;

  const name = document.getElementById('checkoutBuyerName').value || currentUser.name;
  const phone = document.getElementById('checkoutBuyerPhone').value || "+91 98111 22334";
  const address = document.getElementById('checkoutBuyerAddress').value || "Flat 402, Bellandur, Bengaluru";
  const pincode = document.getElementById('checkoutPincodeInput').value || "560103";

  setTimeout(async () => {
    try {
      let totalWageSecured = 0;
      let lastOrderNumber = "";

      for (const item of currentCart) {
        const res = await fetch('/api/orders', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            product_id: item.id,
            quantity: item.quantity || 1,
            buyer_id: currentUser.role === 'BUYER' ? currentUser.id : 1,
            buyer_name: name,
            buyer_phone: phone,
            delivery_address: address,
            delivery_pincode: pincode,
            delivery_city: "Bengaluru",
            delivery_state: "Karnataka",
            payment_method: `DEMO_${currentPaymentTab.toUpperCase()}_ESCROW`
          })
        });
        const orderData = await res.json();
        totalWageSecured += orderData.artisan_wage_secured || 0;
        lastOrderNumber = orderData.order_number;
      }

      currentCart = [];
      saveCart();
      closeModal('demoPaymentModal');
      btn.disabled = false;
      btn.innerHTML = `✨ Authorize & Lock Escrow Payment (Demo)`;

      showToast(`🎉 Payment Secured in Escrow! Order #${lastOrderNumber} created (₹${totalWageSecured.toFixed(0)} protected living wage).`, 'success', 3000);

      navigateTo('view-orders');
      loadOrdersList();
    } catch (e) {
      console.error(e);
      btn.disabled = false;
      btn.innerHTML = `✨ Authorize & Lock Escrow Payment (Demo)`;
      showToast('Error securing escrow payment', 'danger', 2000);
    }
  }, 1200);
}

// 16. Orders List & Respective Artisan/Buyer Role Isolation
async function loadOrdersList() {
  try {
    let url = '/api/orders';
    if (currentUser.role === 'ARTISAN') {
      url = `/api/orders?role=artisan&user_id=${currentUser.id}&artisan_name=${encodeURIComponent(currentUser.name)}`;
    } else if (currentUser.role === 'BUYER') {
      url = `/api/orders?role=buyer&user_id=${currentUser.id}&buyer_name=${encodeURIComponent(currentUser.name)}`;
    } else if (currentUser.role === 'ADMIN') {
      url = `/api/orders?role=admin`;
    }

    const res = await fetch(url);
    const data = await res.json();
    const container = document.getElementById('ordersListContainer');

    if (data.data.length === 0) {
      container.innerHTML = `
        <div style="background: #fff; border: 1px dashed var(--border-color); border-radius: var(--radius-lg); padding: 40px; text-align: center;">
          <div style="font-size: 2.5rem; margin-bottom: 8px;">📦</div>
          <h3 style="margin-bottom: 6px;">No orders found for ${currentUser.name}</h3>
          <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 16px;">
            ${currentUser.role === 'ARTISAN' ? 'When buyers purchase your craft, the order will appear here with instant escrow wage lock.' : 'Explore the fair-trade marketplace to place your first handcrafted order!'}
          </p>
          ${currentUser.role === 'BUYER' ? `<button class="btn-primary" onclick="navigateTo('view-marketplace')">🛍️ Explore Marketplace</button>` : ''}
        </div>
      `;
      return;
    }

    container.innerHTML = data.data.map(ord => {
      let actionButtonsHtml = `<button class="btn-secondary" style="padding: 5px 11px; font-size: 0.78rem;" onclick="openChatModal(${ord.id}, '${ord.artisan_name}', '${ord.buyer_name}')">💬 Open Chat & AI Translation</button>`;

      if (currentUser.role === 'ARTISAN') {
        if (ord.escrow_state === 'PAYMENT_SECURED') {
          actionButtonsHtml += `<button class="btn-primary" style="padding: 5px 11px; font-size: 0.78rem;" onclick="advanceOrderState(${ord.id}, 'ARTISAN_ACCEPTED', 'Artisan verified order specs.')">👩‍🎨 Accept Order</button>`;
        } else if (ord.escrow_state === 'ARTISAN_ACCEPTED') {
          actionButtonsHtml += `<button class="btn-primary" style="padding: 5px 11px; font-size: 0.78rem;" onclick="advanceOrderState(${ord.id}, 'CRAFTING', 'Pitloom weaving started in cluster.')">🧵 Start Crafting</button>`;
        } else if (ord.escrow_state === 'CRAFTING') {
          actionButtonsHtml += `<button class="btn-primary" style="padding: 5px 11px; font-size: 0.78rem;" onclick="advanceOrderState(${ord.id}, 'QUALITY_CHECK', 'GI motif inspection passed.')">🛡️ Pass Quality Check</button>`;
        } else if (ord.escrow_state === 'QUALITY_CHECK') {
          actionButtonsHtml += `<button class="btn-primary" style="padding: 5px 11px; font-size: 0.78rem;" onclick="advanceOrderState(${ord.id}, 'DISPATCHED', 'Package dispatched via India Post SpeedPost.')">🚚 Handover to Logistics</button>`;
        } else if (ord.escrow_state === 'DISPATCHED') {
          actionButtonsHtml += `<span style="color: var(--secondary); font-weight: 600; font-size: 0.8rem; padding: 4px 8px; background: var(--secondary-light); border-radius: 4px;">🚚 In Transit via SpeedPost (AWB: ${ord.tracking_number})</span>`;
        } else if (ord.escrow_state === 'DELIVERED') {
          actionButtonsHtml += `<span style="color: var(--warning); font-weight: 600; font-size: 0.8rem; padding: 4px 8px; background: var(--warning-light); border-radius: 4px;">📦 Delivered. Awaiting Buyer Escrow Release</span>`;
        } else if (ord.escrow_state === 'ESCROW_RELEASED') {
          actionButtonsHtml += `<span style="color: var(--success); font-weight: 700; font-size: 0.82rem; padding: 4px 8px; background: var(--success-light); border-radius: 4px;">✓ ₹${ord.artisan_wage_payout} Released to Bank</span>`;
        }
      } else if (currentUser.role === 'BUYER') {
        if (ord.escrow_state === 'PAYMENT_SECURED') {
          actionButtonsHtml += `<span style="color: var(--info); font-size: 0.8rem; padding: 4px 8px; background: var(--info-light); border-radius: 4px;">🔒 Payment Secured in Escrow. Artisan notified.</span>`;
        } else if (ord.escrow_state === 'ARTISAN_ACCEPTED') {
          actionButtonsHtml += `<span style="color: var(--info); font-size: 0.8rem; padding: 4px 8px; background: var(--info-light); border-radius: 4px;">⏳ Artisan accepted & preparing loom materials.</span>`;
        } else if (ord.escrow_state === 'CRAFTING') {
          actionButtonsHtml += `<span style="color: var(--primary); font-size: 0.8rem; padding: 4px 8px; background: var(--primary-light); border-radius: 4px;">🧵 Artisan is handcrafting your item in workshop.</span>`;
        } else if (ord.escrow_state === 'QUALITY_CHECK') {
          actionButtonsHtml += `<span style="color: var(--secondary); font-size: 0.8rem; padding: 4px 8px; background: var(--secondary-light); border-radius: 4px;">🛡️ GI Authenticity & Quality Check in Progress.</span>`;
        } else if (ord.escrow_state === 'DISPATCHED') {
          actionButtonsHtml += `<button class="btn-primary" style="padding: 5px 11px; font-size: 0.78rem;" onclick="advanceOrderState(${ord.id}, 'DELIVERED', 'Buyer received item.')">📦 Confirm Delivery & Satisfaction</button>`;
        } else if (ord.escrow_state === 'DELIVERED') {
          actionButtonsHtml += `<button class="btn-primary" style="padding: 5px 11px; font-size: 0.78rem; background: var(--success);" onclick="advanceOrderState(${ord.id}, 'ESCROW_RELEASED', 'Buyer confirmed satisfaction. Payout unlocked.')">💰 Release Escrow Payout to Artisan</button>`;
        } else if (ord.escrow_state === 'ESCROW_RELEASED') {
          actionButtonsHtml += `<span style="color: var(--success); font-weight: 700; font-size: 0.82rem; padding: 4px 8px; background: var(--success-light); border-radius: 4px;">✓ Delivered & Escrow Released to Artisan. Thank you for supporting fair living wages!</span>`;
        }
      }

      return `
        <div style="background: #fff; border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 20px; margin-bottom: 20px; box-shadow: var(--shadow-sm);">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
            <div>
              <h3 style="font-size: 1.1rem;">Order #${ord.order_number}</h3>
              <div style="font-size: 0.8rem; color: var(--text-muted);">Placed on ${new Date(ord.created_at).toLocaleDateString()} • Tracking AWB: <b>${ord.tracking_number}</b></div>
            </div>
            <div style="text-align: right;">
              <div style="font-size: 1.25rem; font-weight: 700;">₹${ord.total_amount.toLocaleString('en-IN')}</div>
              <div class="wage-component-badge">🔒 Escrow Wage: ₹${ord.artisan_wage_payout}</div>
            </div>
          </div>

          <div style="display: flex; gap: 14px; margin-bottom: 16px;">
            <img src="${ord.product_image || 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400'}" style="width: 72px; height: 72px; border-radius: var(--radius-md); object-fit: cover;">
            <div style="flex: 1;">
              <div style="font-weight: 600; font-size: 1rem;">${ord.product_title}</div>
              <div style="font-size: 0.82rem; color: var(--text-muted);">Artisan: <b>${ord.artisan_name}</b> • Buyer: <b>${ord.buyer_name}</b> (${ord.delivery_city})</div>
              <div style="margin-top: 4px; font-size: 0.82rem;">Status: <b style="color: var(--primary);">${ord.escrow_state.replace(/_/g, ' ')}</b></div>
            </div>
          </div>

          <!-- State Machine Action Buttons -->
          <div style="display: flex; gap: 8px; flex-wrap: wrap; border-top: 1px dashed var(--border-color); padding-top: 12px; align-items: center;">
            ${actionButtonsHtml}
          </div>
        </div>
      `;
    }).join('');
  } catch (e) {
    console.error("Orders list error:", e);
  }
}

async function advanceOrderState(orderId, nextState, note) {
  try {
    const res = await fetch('/api/orders/transition', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: orderId, new_state: nextState, note: note, actor: currentUser.name })
    });
    if (res.ok) {
      loadOrdersList();
    }
  } catch (e) {
    console.error("State transition error:", e);
  }
}

// 15. Order Chat with AI Translation
function openChatModal(orderId, artisanName, buyerName) {
  activeChatOrderId = orderId;
  document.getElementById('chatModalTitle').innerText = `💬 Chat for Order #${orderId} (${artisanName} ↔ ${buyerName})`;
  refreshChatMessages();
  document.getElementById('chatModal').classList.add('active');
}

async function refreshChatMessages() {
  try {
    const res = await fetch(`/api/chat/${activeChatOrderId}`);
    const data = await res.json();
    const box = document.getElementById('chatMessagesBox');
    box.innerHTML = data.data.map(m => `
      <div style="margin-bottom: 10px; text-align: ${m.sender_role === 'artisan' ? 'left' : 'right'};">
        <div style="display: inline-block; max-width: 80%; background: ${m.sender_role === 'artisan' ? '#fff' : '#ffedd5'}; border: 1px solid #cbd5e1; border-radius: var(--radius-md); padding: 8px 12px; text-align: left;">
          <div style="font-size: 0.72rem; font-weight: bold; color: var(--primary);">${m.sender_name} (${m.sender_role})</div>
          <div style="font-size: 0.9rem;">${m.original_text}</div>
          <div style="font-size: 0.75rem; color: #0f766e; margin-top: 4px; border-top: 1px dashed #cbd5e1; padding-top: 2px;">
            🤖 <i>${m.translated_text}</i>
          </div>
        </div>
      </div>
    `).join('');
    box.scrollTop = box.scrollHeight;
  } catch (e) {
    console.error(e);
  }
}

async function sendChatMessage() {
  const input = document.getElementById('chatMessageInput');
  const text = input.value.trim();
  if (!text) return;

  try {
    await fetch('/api/chat/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_id: activeChatOrderId,
        sender_role: currentUser.role.toLowerCase(),
        sender_name: currentUser.name,
        message: text
      })
    });
    input.value = '';
    refreshChatMessages();
  } catch (e) {
    console.error(e);
  }
}

// 16. Admin Dashboard
async function loadAdminDashboard() {
  try {
    const [metricsRes, artisansRes, demandRes, auditRes] = await Promise.all([
      fetch('/api/admin/metrics'),
      fetch('/api/artisans'),
      fetch('/api/demand-forecasts'),
      fetch('/api/admin/audit-logs')
    ]);

    const metrics = (await metricsRes.json()).data;
    const artisans = (await artisansRes.json()).data;
    const demand = (await demandRes.json()).data;
    const auditLogs = (await auditRes.json()).data;

    document.getElementById('adminMetricsGrid').innerHTML = `
      <div class="pillar-card"><div class="pillar-icon">💰</div><h3>₹${metrics.gross_merchandise_value_inr.toLocaleString('en-IN')}</h3><p>Total Gross Merchandise Value (GMV)</p></div>
      <div class="pillar-card"><div class="pillar-icon">⚖️</div><h3>₹${metrics.artisan_protected_earnings_inr.toLocaleString('en-IN')}</h3><p>Artisan Living Wages Protected</p></div>
      <div class="pillar-card"><div class="pillar-icon">🔒</div><h3>₹${metrics.active_escrow_held_inr.toLocaleString('en-IN')}</h3><p>Active Escrow Vault Balance</p></div>
      <div class="pillar-card"><div class="pillar-icon">👩‍🎨</div><h3>${metrics.total_artisans} (${metrics.verified_artisans} Verified)</h3><p>Total Onboarded Artisans</p></div>
    `;

    document.getElementById('adminArtisanTableBody').innerHTML = artisans.map(a => `
      <tr>
        <td><b>${a.name}</b></td>
        <td>${a.state_cluster}</td>
        <td>${a.specific_craft}</td>
        <td><span class="gi-tag-pill" style="position: static;">${a.verification_status}</span></td>
        <td>
          <button class="btn-secondary" style="padding: 3px 8px; font-size: 0.75rem;" onclick="reviewArtisanAction(${a.id}, 'approve')">✓ Approve</button>
          <button class="btn-secondary" style="padding: 3px 8px; font-size: 0.75rem; color: var(--danger);" onclick="reviewArtisanAction(${a.id}, 'reject')">✕ Reject</button>
        </td>
      </tr>
    `).join('');

    document.getElementById('adminDemandGrid').innerHTML = demand.map(d => `
      <div style="background: #f8fafc; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 14px;">
        <div style="font-weight: 700; color: var(--primary); font-size: 1rem;">${d.craft_category} (${d.region})</div>
        <div style="font-size: 1.1rem; font-weight: bold; color: var(--success); margin: 3px 0;">+${d.growth_pct}% Projected Surge</div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">Suggested Production: <b>+${d.suggested_units} units</b></div>
        <div style="font-size: 0.78rem; margin-top: 6px; color: #475569;">${d.reasons.join(' • ')}</div>
      </div>
    `).join('');

    document.getElementById('adminAuditLogBody').innerHTML = auditLogs.map(l => `
      <tr>
        <td style="font-size: 0.78rem;">${new Date(l.timestamp).toLocaleTimeString()}</td>
        <td><b>${l.admin_name}</b></td>
        <td>${l.action_type}</td>
        <td>${l.entity_type} #${l.entity_id}</td>
        <td><span style="color: var(--text-muted);">${l.previous_state || '-'}</span> → <b>${l.new_state}</b></td>
        <td style="font-size: 0.8rem;">${l.reason}</td>
      </tr>
    `).join('');
  } catch (e) {
    console.error("Admin dashboard error:", e);
  }
}

async function reviewArtisanAction(artisanId, action) {
  try {
    await fetch('/api/admin/review-artisan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ artisan_id: artisanId, action: action, admin_name: currentUser.name })
    });
    loadAdminDashboard();
  } catch (e) {
    console.error(e);
  }
}

async function reseedDemoDatabase() {
  if (confirm("Reset and reseed database with 8 Artisans, 6 Buyers, and verified orders?")) {
    try {
      const res = await fetch('/api/admin/reseed', { method: 'POST' });
      if (res.ok) {
        alert("Database reseeded successfully!");
        loadAdminDashboard();
        loadOrdersList();
      }
    } catch (e) {
      console.error(e);
    }
  }
}

// 17. Public Impact Dashboard & Transparency Ledger
const STATE_CLUSTERS_DATA = [
  { state: "Maharashtra", artisan: "Rishikant Mishra", craft: "Paithani Silk Weaving", gi: "GI-MH-001", wage: "₹65.00/hr", women: "74%", rating: "⭐⭐⭐⭐⭐ (100% Organic Mulberry)" },
  { state: "Bihar", artisan: "Meenakshi Jha", craft: "Madhubani Mithila Art", gi: "GI-BR-002", wage: "₹62.00/hr", women: "92%", rating: "⭐⭐⭐⭐⭐ (Natural Vegetable Dyes)" },
  { state: "Rajasthan", artisan: "Devendra Sharma", craft: "Jaipur Blue Pottery", gi: "GI-RJ-003", wage: "₹65.00/hr", women: "58%", rating: "⭐⭐⭐⭐⭐ (Lead-Free Quartz)" },
  { state: "Odisha", artisan: "Gurucharan Mohapatra", craft: "Dhokra Lost-Wax Metallurgy", gi: "GI-OD-004", wage: "₹60.00/hr", women: "65%", rating: "⭐⭐⭐⭐⭐ (Recycled Bell Metal)" },
  { state: "Tamil Nadu", artisan: "Kalyanasundaram Swamy", craft: "Kanchipuram Silk Korvai", gi: "GI-TN-005", wage: "₹68.00/hr", women: "61%", rating: "⭐⭐⭐⭐⭐ (Pure Silk Mark Verified)" },
  { state: "Assam", artisan: "Debabrata Saikia", craft: "Organic Bamboo & Cane", gi: "GI-AS-008", wage: "₹58.00/hr", women: "80%", rating: "⭐⭐⭐⭐⭐ (Zero Plastic Sustainable)" },
  { state: "West Bengal", artisan: "Moumita Banerjee", craft: "Nakshi Kantha Embroidery", gi: "GI-WB-006", wage: "₹55.00/hr", women: "96%", rating: "⭐⭐⭐⭐⭐ (Handspun Tussar)" },
  { state: "Jammu & Kashmir", artisan: "Ghulam Mohammad Mir", craft: "Pashmina Cashmere Sozni", gi: "GI-JK-007", wage: "₹75.00/hr", women: "70%", rating: "⭐⭐⭐⭐⭐ (100% Changthangi Cashmere)" }
];

async function loadPublicImpactData() {
  try {
    const res = await fetch('/api/admin/metrics');
    const data = (await res.json()).data;

    // 1. 6 Pillars Grid
    const metricsGrid = document.getElementById('publicImpactMetricsGrid');
    if (metricsGrid) {
      metricsGrid.innerHTML = `
        <div class="impact-stat-box">
          <div class="impact-stat-header">
            <span class="impact-stat-title">Protected Living Wages</span>
            <div class="impact-stat-icon" style="background: #f0fdf4; color: #16a34a;">⚖️</div>
          </div>
          <div class="impact-stat-val" style="color: #16a34a;">₹${data.artisan_protected_earnings_inr.toLocaleString('en-IN')}</div>
          <div class="impact-stat-sub">Direct bank transfers to rural creators under statutory living wage algorithmic floors.</div>
        </div>

        <div class="impact-stat-box">
          <div class="impact-stat-header">
            <span class="impact-stat-title">Middleman Extraction Eliminated</span>
            <div class="impact-stat-icon" style="background: #eff6ff; color: #2563eb;">🚫</div>
          </div>
          <div class="impact-stat-val" style="color: #2563eb;">₹${data.middleman_leakage_prevented_inr.toLocaleString('en-IN')}</div>
          <div class="impact-stat-sub">35–65% traditional wholesale leakage bypassed through direct open ONDC network routing.</div>
        </div>

        <div class="impact-stat-box">
          <div class="impact-stat-header">
            <span class="impact-stat-title">GI Authenticity Protection</span>
            <div class="impact-stat-icon" style="background: #fefce8; color: #ca8a04;">🛡️</div>
          </div>
          <div class="impact-stat-val" style="color: #ca8a04;">100% Verified</div>
          <div class="impact-stat-sub">Every product cataloged is cross-verified against the National Geographical Indication Registry.</div>
        </div>

        <div class="impact-stat-box">
          <div class="impact-stat-header">
            <span class="impact-stat-title">Rural Women Empowerment</span>
            <div class="impact-stat-icon" style="background: #fdf2f8; color: #db2777;">👩‍🎨</div>
          </div>
          <div class="impact-stat-val" style="color: #db2777;">74.5% Active</div>
          <div class="impact-stat-sub">Guild representation across Kantha, Madhubani & Paithani self-help artisan clusters.</div>
        </div>

        <div class="impact-stat-box">
          <div class="impact-stat-header">
            <span class="impact-stat-title">Sustainable & Zero Carbon</span>
            <div class="impact-stat-icon" style="background: #f0fdfa; color: #0d9488;">🌱</div>
          </div>
          <div class="impact-stat-val" style="color: #0d9488;">100% Eco-Craft</div>
          <div class="impact-stat-sub">100% natural vegetable dyes, handloom pitlooms, raw bamboo & non-toxic recycled bell metals.</div>
        </div>

        <div class="impact-stat-box">
          <div class="impact-stat-header">
            <span class="impact-stat-title">Pan-India Logistics Reach</span>
            <div class="impact-stat-icon" style="background: #f5f3ff; color: #7c3aed;">🚚</div>
          </div>
          <div class="impact-stat-val" style="color: #7c3aed;">19,100+ PINs</div>
          <div class="impact-stat-sub">Integrated SpeedPost & ONDC unified logistics adapters for rural-to-urban delivery.</div>
        </div>
      `;
    }

    // 2. State Clusters Table
    const tableBody = document.getElementById('impactClustersTableBody');
    if (tableBody) {
      tableBody.innerHTML = STATE_CLUSTERS_DATA.map(c => `
        <tr>
          <td><b>📍 ${c.state}</b></td>
          <td>${c.artisan}</td>
          <td><b>${c.craft}</b></td>
          <td><span class="gi-tag-pill" style="position: static;">${c.gi}</span></td>
          <td style="color: var(--success); font-weight: 700;">${c.wage}</td>
          <td><span style="background: #fdf2f8; color: #db2777; font-weight: 600; padding: 2px 6px; border-radius: 4px; font-size: 0.78rem;">${c.women} Women</span></td>
          <td style="font-size: 0.8rem; color: #059669;">${c.rating}</td>
        </tr>
      `).join('');
    }

    // 3. Live Escrow Stream Ledger
    const ledgerBox = document.getElementById('impactEscrowLedgerBox');
    if (ledgerBox) {
      const ordersRes = await fetch('/api/orders?role=admin');
      const orders = (await ordersRes.json()).data;

      ledgerBox.innerHTML = orders.slice(0, 6).map(o => `
        <div style="background: #f8fafc; border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
          <div>
            <div style="font-weight: 700; font-size: 0.88rem; display: flex; align-items: center; gap: 8px;">
              <span>📜 Order #${o.order_number}</span>
              <span class="badge-escrow" style="font-size: 0.72rem;">${o.escrow_state}</span>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">
              Buyer: <b>${o.buyer_name}</b> ➔ Artisan: <b>${o.artisan_name}</b> (${o.product_title ? o.product_title.slice(0, 32) : 'Handcrafted Item'}...)
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-weight: 800; color: var(--primary); font-size: 0.95rem;">₹${o.total_amount.toLocaleString('en-IN')}</div>
            <div style="font-size: 0.75rem; color: var(--success); font-weight: 600;">⚖️ ₹${o.artisan_wage_payout} Protected Wage</div>
          </div>
        </div>
      `).join('');
    }
  } catch (e) {
    console.error("Public impact error:", e);
  }
}

// 18. Search and AI Natural Language Filters
function executeMarketplaceSearch() {
  const query = document.getElementById('marketplaceSearchInput').value;
  loadMarketplaceProducts(query);
}

function applyQuickFilter(type) {
  const input = document.getElementById('marketplaceSearchInput');
  if (type === 'gi') input.value = "GI Certified";
  else if (type === 'maharashtra') input.value = "Maharashtra Paithani";
  else if (type === 'bihar') input.value = "Bihar Madhubani";
  else if (type === 'rajasthan') input.value = "Rajasthan Blue Pottery";
  else if (type === 'tamilnadu') input.value = "Tamil Nadu Kanchipuram";
  else if (type === 'under2000') input.value = "Under 2000";
  else if (type === 'reset') input.value = "";
  executeMarketplaceSearch();
}

// 19. Modals Helpers
function closeModal(modalId) {
  document.getElementById(modalId).classList.remove('active');
}

function openAssistantModal() {
  document.getElementById('assistantModal').classList.add('active');
}

async function queryAssistant() {
  const input = document.getElementById('assistantInput');
  const query = input.value.trim();
  if (!query) return;

  const history = document.getElementById('assistantHistory');
  history.innerHTML += `<div style="font-size: 0.88rem; font-weight: bold; margin-top: 8px; color: var(--primary);">Q: ${query}</div>`;

  try {
    const res = await fetch('/api/assistant/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_role: currentUser.role, query: query })
    });
    const data = await res.json();
    history.innerHTML += `<div style="font-size: 0.88rem; color: #334155; margin-top: 4px; background: #fff; padding: 8px; border-radius: 6px; border: 1px solid #e2e8f0;">💡 ${data.data.answer}</div>`;
    input.value = '';
    history.scrollTop = history.scrollHeight;
  } catch (e) {
    console.error(e);
  }
}

async function openONDCModal() {
  try {
    const res = await fetch('/api/export-ondc', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ craft_data: CRAFT_PRESETS.paithani, artisan_name: "Rishikant Mishra", artisan_region: "Maharashtra" })
    });
    const data = await res.json();
    document.getElementById('ondcSchemaDisplay').innerText = JSON.stringify(data.data, null, 2);
    document.getElementById('ondcModal').classList.add('active');
  } catch (e) {
    console.error(e);
  }
}

function openGICertificateModal() {
  const modalBody = document.getElementById('giCertModalBody');
  modalBody.innerHTML = `
    <div><b>GI Registry Tag:</b> GI-MH-001</div>
    <div><b>Craft Name:</b> Paithani Sarees & Handloom Fabrics</div>
    <div><b>Authorized Body:</b> Yeola Paithani Weavers Guild</div>
    <div><b>Registration Year:</b> 2010 (Renewed & Active)</div>
    <div><b>Geographical Origin:</b> Yeola, Nashik District, Maharashtra</div>
    <div style="margin-top: 10px; font-size: 0.78rem; color: var(--success);">
      ✓ Cryptographic checksum verified against National Intellectual Property Office.
    </div>
  `;
  document.getElementById('giCertModal').classList.add('active');
}

function openMarketingKitModal() {
  if (currentExtractedData && currentExtractedData.marketing_kit) {
    document.getElementById('mktWhatsAppText').value = currentExtractedData.marketing_kit.whatsapp_broadcast;
    document.getElementById('mktInstaText').value = currentExtractedData.marketing_kit.instagram_caption;
  }
  document.getElementById('marketingModal').classList.add('active');
}

function copyToClipboard(elementId) {
  const copyText = document.getElementById(elementId);
  copyText.select();
  document.execCommand('copy');
  showToast("📋 Copied to clipboard!", "success", 2000);
}

// Global Init on DOM Load
window.addEventListener('DOMContentLoaded', () => {
  updateRoleAccess(currentUser.role);
  updateCartBadge();
  updateWishlistBadge();
  loadFeaturedProducts();
  loadPreset('paithani');
  initDragAndDrop();
});

