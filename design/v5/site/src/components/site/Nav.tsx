import { useEffect, useRef, useState } from "react";
import { NAV } from "@/content/site";
import { SITE } from "@/config/site";
import { Logo } from "./ui/Logo";
import { Button } from "./ui/Button";

export function Nav() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [active, setActive] = useState("");
  const toggle = useRef<HTMLButtonElement>(null);
  const menu = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    if (typeof IntersectionObserver === "undefined") return;
    const sections = NAV.map((n) => document.getElementById(n.id)).filter(
      (el): el is HTMLElement => el !== null,
    );
    if (!sections.length) return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) if (entry.isIntersecting) setActive(entry.target.id);
      },
      { rootMargin: "-45% 0px -50% 0px" },
    );
    sections.forEach((s) => observer.observe(s));
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!open) return;
    const outside = [document.getElementById("main"), document.querySelector("footer")];
    outside.forEach((el) => el?.setAttribute("inert", ""));
    const priorOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpen(false);
        toggle.current?.focus();
      }
    };
    const onResize = () => {
      if (window.innerWidth > 860) setOpen(false);
    };
    document.addEventListener("keydown", onKey);
    window.addEventListener("resize", onResize);
    return () => {
      outside.forEach((el) => el?.removeAttribute("inert"));
      document.body.style.overflow = priorOverflow;
      document.removeEventListener("keydown", onKey);
      window.removeEventListener("resize", onResize);
    };
  }, [open]);

  return (
    <>
      <header className={`nav ${scrolled || open ? "is-scrolled" : ""}`}>
        <div className="wrap nav-inner">
          <a className="logo" href="/#top" aria-label="RN INVEST, zur Startseite">
            <Logo />
          </a>
          <nav className="nav-links micro" aria-label="Hauptnavigation">
            {NAV.map((n) => (
              <a key={n.id} href={`/#${n.id}`} aria-current={active === n.id ? "true" : undefined}>
                {n.label}
              </a>
            ))}
          </nav>
          <button
            ref={toggle}
            type="button"
            className="menu-toggle micro"
            aria-expanded={open}
            aria-controls="mobile-menu"
            onClick={() => setOpen((v) => !v)}
          >
            <span>{open ? "Schließen" : "Menü"}</span>
            <span className="bars" aria-hidden="true">
              <i />
              <i />
            </span>
          </button>
        </div>
      </header>
      {open && (
        <div ref={menu} id="mobile-menu" className="menu">
          <nav aria-label="Mobile Navigation">
            <ol>
              {NAV.map((n) => (
                <li key={n.id}>
                  <a href={`/#${n.id}`} onClick={() => setOpen(false)}>
                    {n.label}
                  </a>
                </li>
              ))}
            </ol>
          </nav>
          <div className="menu-foot">
            <Button href="/#kontakt" solid onClick={() => setOpen(false)}>
              Objekt anbieten
            </Button>
            <a className="micro muted" href={`mailto:${SITE.email}`}>
              {SITE.email}
            </a>
          </div>
        </div>
      )}
    </>
  );
}
