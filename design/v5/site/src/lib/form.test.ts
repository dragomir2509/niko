import { describe, expect, it } from "vitest";
import { buildMailto, MESSAGES, normalize, subjectFor, validate, type FormValues } from "./form";

const base: FormValues = {
  formType: "property",
  name: "A",
  email: "a@b.de",
  phone: "",
  location: "Pasing",
  propertyType: "Grundstück",
  exposeUrl: "",
  message: "",
  consent: true,
};

describe("property offer", () => {
  it("accepts an offer without optional fields", () => expect(validate(base)).toEqual({}));
  it("requires a name", () => expect(validate({ ...base, name: " " }).name).toBe(MESSAGES.name));
  it("requires a valid email", () =>
    expect(validate({ ...base, email: "x" }).email).toBe(MESSAGES.email));
  it("requires consent", () =>
    expect(validate({ ...base, consent: false }).consent).toBe(MESSAGES.consent));
  it("requires a location", () =>
    expect(validate({ ...base, location: "" }).location).toBe(MESSAGES.location));
  it("requires a known property type", () => {
    expect(validate({ ...base, propertyType: "" }).propertyType).toBe(MESSAGES.propertyType);
    expect(validate({ ...base, propertyType: "Schloss" }).propertyType).toBe(MESSAGES.propertyType);
  });
  it("rejects non-HTTP exposé links", () =>
    expect(validate({ ...base, exposeUrl: "javascript:alert(1)" }).exposeUrl).toBe(
      MESSAGES.exposeUrl,
    ));
  it("accepts an optional HTTPS exposé link", () =>
    expect(validate({ ...base, exposeUrl: "https://example.de/expose" })).toEqual({}));
  it("rejects line breaks in single-line fields (header injection)", () => {
    expect(validate({ ...base, name: "A\r\nBcc: x@y.de" }).name).toBe(MESSAGES.singleLine);
    expect(validate({ ...base, location: "Pasing\nSubject: x" }).location).toBe(
      MESSAGES.singleLine,
    );
  });
});

describe("general enquiry", () => {
  const general: FormValues = { ...base, formType: "general", location: "", propertyType: "" };
  it("needs only name, email and consent", () => expect(validate(general)).toEqual({}));
  it("drops property-only fields", () =>
    expect(normalize({ ...base, formType: "general" })).toMatchObject({
      location: "",
      propertyType: "",
      exposeUrl: "",
    }));
});

describe("mail helpers", () => {
  it("builds a single-line subject", () => {
    expect(subjectFor(base)).toBe("Objektangebot: Pasing");
    expect(subjectFor({ formType: "general", location: "", name: "A\nB" })).toBe(
      "Allgemeine Anfrage: A B",
    );
  });
  it("builds a mailto fallback with the entered data", () => {
    const href = buildMailto("rn@rninvest.de", { ...base, message: "Hallo" });
    expect(href.startsWith("mailto:rn@rninvest.de?subject=")).toBe(true);
    expect(decodeURIComponent(href)).toContain("Objektart: Grundstück");
    expect(decodeURIComponent(href)).toContain("Nachricht:\nHallo");
  });
});
