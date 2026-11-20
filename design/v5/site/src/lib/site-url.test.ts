import { describe, expect, it } from "vitest";
import { getSiteUrl } from "./site-url";

describe("Public site URL", () => {
  it("uses the published RN INVEST URL for bracket placeholders", () => {
    expect(getSiteUrl("https://[domain]")).toBe("https://rn-invest-muenchen.lovable.app");
  });
  it("uses a real configured HTTP URL", () => {
    expect(getSiteUrl("https://rn-invest.example/")).toBe("https://rn-invest.example");
    expect(getSiteUrl("http://rn-invest.example")).toBe("http://rn-invest.example");
  });
  it("falls back for missing or invalid URLs", () => {
    expect(getSiteUrl("")).toBe("https://rn-invest-muenchen.lovable.app");
    expect(getSiteUrl("http-not-a-url")).toBe("https://rn-invest-muenchen.lovable.app");
    expect(getSiteUrl("ftp://rn-invest.example")).toBe("https://rn-invest-muenchen.lovable.app");
  });
});