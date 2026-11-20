import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
const { send } = vi.hoisted(() => ({ send: vi.fn() }));
vi.mock("@tanstack/react-start", () => ({
  useServerFn: () => send,
  createServerFn: () => ({ validator: () => ({ handler: () => vi.fn() }) }),
}));
vi.mock("@tanstack/react-start/server", () => ({ getRequestHeader: () => undefined }));
import { Kontakt } from "@/components/site/Kontakt";

function fill() {
  fireEvent.change(screen.getByLabelText("Objektadresse oder Lage *"), {
    target: { value: "Gräfelfing" },
  });
  fireEvent.change(screen.getByLabelText("Objektart *"), { target: { value: "Grundstück" } });
  fireEvent.change(screen.getByLabelText("Name *"), { target: { value: "Test" } });
  fireEvent.change(screen.getByLabelText("E-Mail *"), { target: { value: "test@example.de" } });
  fireEvent.click(document.getElementById("f-consent") as HTMLInputElement);
}
const submit = () => fireEvent.submit(document.querySelector("form") as HTMLFormElement);

beforeEach(() => send.mockReset());

describe("contact form outcome", () => {
  it("confirms only after the server accepted the request", async () => {
    send.mockResolvedValue({ ok: true });
    render(<Kontakt />);
    fill();
    submit();
    await screen.findByRole("status");
    expect(send).toHaveBeenCalledWith(
      expect.objectContaining({
        data: expect.objectContaining({
          values: expect.objectContaining({
            formType: "property",
            location: "Gräfelfing",
            propertyType: "Grundstück",
          }),
        }),
      }),
    );
  });
  it("shows no success and keeps the data when delivery is unavailable", async () => {
    send.mockResolvedValue({ ok: false, code: "unavailable", error: "Nicht verfügbar" });
    render(<Kontakt />);
    fill();
    submit();
    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("Nicht verfügbar");
    expect(screen.queryByRole("status")).toBeNull();
    expect(screen.getByLabelText("Name *")).toHaveValue("Test");
    expect(screen.getByRole("link", { name: "E-Mail mit diesen Angaben öffnen" })).toHaveAttribute(
      "href",
      expect.stringContaining("mailto:rn@rninvest.de"),
    );
  });
  it("does not call the server with invalid input", () => {
    render(<Kontakt />);
    submit();
    expect(send).not.toHaveBeenCalled();
    expect(screen.getByLabelText("Objektadresse oder Lage *")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
  });
  it("adapts the fields to a general enquiry", () => {
    render(<Kontakt />);
    fireEvent.click(screen.getByLabelText("Allgemeine Anfrage"));
    expect(screen.queryByLabelText("Objektadresse oder Lage *")).toBeNull();
    expect(screen.queryByLabelText("Objektart *")).toBeNull();
    expect(screen.getByLabelText("Name *")).toBeInTheDocument();
  });
});
