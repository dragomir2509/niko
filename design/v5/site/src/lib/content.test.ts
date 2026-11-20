import { describe, expect, it } from "vitest";
import { ALL_PLACES, CONTENT, MFH_MAX_PURCHASE_PRICE, NAV } from "@/content/site";
import { SITE } from "@/config/site";
import { monthLabel } from "./date";

describe("company data", () => {
  it("uses the official identity", () => {
    expect(SITE.legalName).toBe("RN Invest UG (haftungsbeschränkt)");
    expect(SITE.managingDirector).toBe("Niko Roncevic");
    expect(`${SITE.street}, ${SITE.postalCode} ${SITE.city}`).toBe(
      "Lochhamer Schlag 12, 82166 Gräfelfing",
    );
    expect(`${SITE.registerCourt}, ${SITE.registerNumber}`).toBe("Amtsgericht München, HRB 305629");
    expect(SITE.email).toBe("rn@rninvest.de");
    expect(SITE.phone).toBe("");
  });
  it("contains no placeholders", () => {
    expect(JSON.stringify({ SITE, CONTENT })).not.toMatch(
      /\[[A-Za-zÄÖÜäöüß .-]+\]|TODO|Platzhalter/,
    );
  });
});

describe("acquisition profile", () => {
  it("keeps the search locations", () => {
    expect(CONTENT.profile.a.city).toHaveLength(9);
    expect(CONTENT.profile.a.county).toEqual(["Gräfelfing", "Pullach", "Grünwald"]);
    expect(CONTENT.profile.b.city).toHaveLength(7);
    expect(ALL_PLACES).toHaveLength(18);
  });
  it("states the purchase price limit for apartment buildings only", () => {
    expect(MFH_MAX_PURCHASE_PRICE).toBe(5_000_000);
    expect(`${CONTENT.profile.b.price.label}: ${CONTENT.profile.b.price.value}`).toBe(
      "Ankaufspreis: bis 5.000.000 €",
    );
    expect(CONTENT.profile.b.price.note).toBe("gilt für Mehrfamilienhäuser");
    expect(JSON.stringify(CONTENT.profile.a)).not.toContain("5.000.000");
  });
});

describe("site rules", () => {
  it("offers the four primary navigation targets", () =>
    expect(NAV.map((n) => n.label)).toEqual([
      "Über RN INVEST",
      "Investmentansatz",
      "Ankaufsprofil",
      "Kontakt",
    ]));
  it("does not address investors or use the first person plural", () =>
    expect(JSON.stringify(CONTENT)).not.toMatch(
      /\b(wir|uns|unser\w*|Investor\w*|Kapitalgeber)\b/i,
    ));
  it("introduces the managing director without repeating the legal entity", () => {
    expect(CONTENT.about.person.name).toBe("Niko Roncevic");
    expect(JSON.stringify(CONTENT.about)).not.toContain("UG (haftungsbeschränkt)");
  });
  it("formats the dossier date", () =>
    expect(monthLabel(new Date("2026-11-19T23:20:00Z"))).toBe("11/2026"));
});
