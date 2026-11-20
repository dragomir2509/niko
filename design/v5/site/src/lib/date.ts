/** Numeric month label for dossier metadata, e.g. "11/2026". */
export function monthLabel(date = new Date()) {
  return `${String(date.getUTCMonth() + 1).padStart(2, "0")}/${date.getUTCFullYear()}`;
}
