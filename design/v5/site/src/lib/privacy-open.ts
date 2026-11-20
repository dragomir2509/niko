const OPEN_EVENT = "rn:privacy-open";

/** Opens the privacy settings dialog from anywhere on the site. */
export function openPrivacySettings() {
  window.dispatchEvent(new Event(OPEN_EVENT));
}

export function onPrivacyOpen(listener: () => void): () => void {
  window.addEventListener(OPEN_EVENT, listener);
  return () => window.removeEventListener(OPEN_EVENT, listener);
}
