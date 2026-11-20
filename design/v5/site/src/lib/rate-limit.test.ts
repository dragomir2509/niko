import { beforeEach, describe, expect, it } from "vitest";
import { allowRequest, markDelivered, resetRateLimit, wasDelivered } from "./rate-limit.server";

beforeEach(() => resetRateLimit());

describe("contact rate limit", () => {
  it("allows five requests per client in ten minutes, then blocks", () => {
    const t = 1_000_000;
    for (let i = 0; i < 5; i++) expect(allowRequest("1.2.3.4", t + i)).toBe(true);
    expect(allowRequest("1.2.3.4", t + 10)).toBe(false);
    expect(allowRequest("5.6.7.8", t + 10)).toBe(true);
  });
  it("frees the client after the window", () => {
    const t = 1_000_000;
    for (let i = 0; i < 5; i++) allowRequest("1.2.3.4", t);
    expect(allowRequest("1.2.3.4", t + 10 * 60 * 1000 + 1)).toBe(true);
  });
  it("caps the whole site per hour", () => {
    const t = 1_000_000;
    for (let i = 0; i < 40; i++) expect(allowRequest(`c${i}`, t)).toBe(true);
    expect(allowRequest("another", t + 1)).toBe(false);
  });
  it("remembers delivered request ids", () => {
    expect(wasDelivered("a")).toBe(false);
    markDelivered("a");
    expect(wasDelivered("a")).toBe(true);
  });
});
