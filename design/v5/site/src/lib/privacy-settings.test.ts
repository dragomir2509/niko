import { describe, expect, it } from "vitest";
import { mayLoadOptional, savePrivacyChoices, PRIVACY_VERSION } from "./privacy-settings";
it("blocks every unregistered optional purpose even after a saved grant", async () => {
  savePrivacyChoices({ analytics: "granted", advertising: "granted" });
  expect(await mayLoadOptional("analytics")).toBe(false);
  expect(await mayLoadOptional("advertising")).toBe(false);
});
it("records choice version and time locally", () => {
  savePrivacyChoices({ analytics: "denied" });
  const receipt = JSON.parse(localStorage.getItem("rn_privacy_receipt") ?? "null");
  expect(receipt.version).toBe(PRIVACY_VERSION);
  expect(receipt.choices.analytics).toBe("denied");
  expect(Number.isFinite(Date.parse(receipt.at))).toBe(true);
});
