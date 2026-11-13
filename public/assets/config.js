// Site-wide settings. Fill these in before launch – see README.md.
window.CJR_CONFIG = {
  // Klaviyo > Settings > Account > API keys > Public API key (6 characters)
  klaviyoPublicKey: 'VWaT2W',
  // Klaviyo > Audience > Lists & Segments > your waitlist list > Settings > List ID
  klaviyoListId: 'T6wqYA',
  // Meta Events Manager > Data sources > your pixel > Pixel ID (15–16 digits)
  metaPixelId: '964454943005948',
  // Google Analytics > Admin > Data streams > your web stream > Measurement ID (G-…)
  ga4MeasurementId: 'G-YRQLZNN803',
  // TikTok Ads Manager > Assets > Events > Web events > your pixel > Pixel ID.
  // One pixel per TikTok ad account. Leave empty until the account exists (nothing loads).
  tiktokPixelIdCjr: '',       // CJane Run account: used on every page except /everyday/ and /privacy/
  tiktokPixelIdEveryday: ''   // Everyday account: used on /everyday/ pages
};
