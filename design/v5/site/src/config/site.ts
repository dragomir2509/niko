/** Official company data. Single source for imprint, contact, footer and structured data. */
export const SITE = {
  name: "RN INVEST",
  /** Public origin of the published site. Update when a custom domain is connected. */
  url: "https://rn-invest-muenchen.lovable.app",
  legalName: "RN Invest UG (haftungsbeschränkt)",
  managingDirector: "Niko Roncevic",
  founder: "Niko Roncevic",
  street: "Lochhamer Schlag 12",
  postalCode: "82166",
  city: "Gräfelfing",
  country: "Deutschland",
  countryCode: "DE",
  registerCourt: "Amtsgericht München",
  registerNumber: "HRB 305629",
  email: "rn@rninvest.de",
  /** Intentionally empty: RN INVEST does not publish a phone number. */
  phone: "",
  geo: { lat: 48.1167, lng: 11.4333 },
} as const;
