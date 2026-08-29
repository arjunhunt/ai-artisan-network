/* ==============================================================================
   AI ARTISAN COMMERCE NETWORK - OFFLINE / LOW-BANDWIDTH DRAFT MANAGER
   ============================================================================== */

const OFFLINE_STORAGE_KEY = "artisan_offline_drafts_v1";

const OfflineDraftManager = {
  saveDraft(draftData) {
    try {
      const drafts = this.getAllDrafts();
      const draftRecord = {
        ...draftData,
        draft_id: `DRAFT-${Date.now()}`,
        saved_at: new Date().toISOString(),
        synced: false
      };
      drafts.unshift(draftRecord);
      localStorage.setItem(OFFLINE_STORAGE_KEY, JSON.stringify(drafts));
      this.updateSyncBadge();
      return draftRecord;
    } catch (e) {
      console.warn("Offline storage error:", e);
      return null;
    }
  },

  getAllDrafts() {
    try {
      const item = localStorage.getItem(OFFLINE_STORAGE_KEY);
      return item ? JSON.parse(item) : [];
    } catch (e) {
      return [];
    }
  },

  updateSyncBadge() {
    const drafts = this.getAllDrafts().filter(d => !d.synced);
    const badge = document.getElementById('offlineSyncBadge');
    if (badge) {
      if (drafts.length > 0) {
        badge.style.display = 'inline-flex';
        badge.innerHTML = `📡 <b>${drafts.length}</b> draft(s) cached offline`;
      } else {
        badge.style.display = 'none';
      }
    }
  },

  async syncAllDrafts() {
    if (!navigator.onLine) {
      if (typeof showToast === 'function') showToast("Device is currently offline. Will sync when connection restores.", "warning", 2000);
      return;
    }
    const drafts = this.getAllDrafts().filter(d => !d.synced);
    if (drafts.length === 0) {
      if (typeof showToast === 'function') showToast("All artisan drafts are already synchronized with server.", "info", 2000);
      return;
    }

    let syncedCount = 0;
    for (const draft of drafts) {
      try {
        const res = await fetch("/api/products", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(draft)
        });
        if (res.ok) {
          draft.synced = true;
          syncedCount++;
        }
      } catch (e) {
        console.error("Failed to sync draft:", e);
      }
    }

    localStorage.setItem(OFFLINE_STORAGE_KEY, JSON.stringify(drafts));
    this.updateSyncBadge();
    if (typeof showToast === 'function') showToast(`Successfully synchronized ${syncedCount} offline craft listing(s)!`, "success", 2500);
  }
};

window.addEventListener('online', () => {
  console.log("🌐 Network online. Syncing drafts...");
  OfflineDraftManager.syncAllDrafts();
});

window.addEventListener('load', () => {
  OfflineDraftManager.updateSyncBadge();
});
