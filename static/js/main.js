/**
 * TRAnime - İstemci Taraflı JavaScript Fonksiyonları
 * Modüler, hafif ve saf JavaScript (Vanilla JS)
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Arama Kutusuna 'Ctrl + K' Kısayolu ile Odaklanma
  const searchInput = document.querySelector('.topbar-search input') || document.querySelector('.search-box input');
  
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
    }
  });

  // 2. Slider Göstergeleri (Dots)
  const dots = document.querySelectorAll('.slider-dots .dot');
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      dots.forEach(d => d.classList.remove('active'));
      dot.classList.add('active');
    });
  });

  // 3. Kart Tıklama Etkileşimi
  const animeCards = document.querySelectorAll('.anime-card');
  animeCards.forEach(card => {
    card.addEventListener('click', () => {
      const title = card.querySelector('.card-title')?.innerText || 'Anime';
      console.log(`[TRAnime] Seçilen anime: ${title}`);
    });
  });

  console.log('[TRAnime] Modern Streaming Dashboard hazır.');
});
