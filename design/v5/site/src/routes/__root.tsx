import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  createRootRouteWithContext,
  useRouter,
  HeadContent,
  Scripts,
  type ErrorComponentProps,
} from "@tanstack/react-router";
import { useEffect, type ReactNode } from "react";

import appCss from "../styles.css?url";
import archivoFont from "../assets/fonts/archivo-latin-wdth-normal.woff2?url";
import { reportLovableError } from "../lib/lovable-error-reporting";
import { CONTENT } from "@/content/site";
import { Button } from "@/components/site/ui/Button";
import { Monogram } from "@/components/site/ui/Logo";

function NotFoundComponent() {
  return (
    <main className="error-screen">
      <div className="wrap">
        <Monogram size="text" className="error-mark" />
        <p className="mono">404</p>
        <h1>{CONTENT.errorPage.notFound}</h1>
        <div className="error-actions">
          <Button href="/" solid>
            {CONTENT.errorPage.home}
          </Button>
        </div>
      </div>
    </main>
  );
}

export function ErrorComponent({ error, reset }: ErrorComponentProps) {
  console.error(error);
  const router = useRouter();
  useEffect(() => {
    reportLovableError(error, { boundary: "tanstack_root_error_component" });
  }, [error]);

  return (
    <main className="error-screen">
      <div className="wrap">
        <Monogram size="text" className="error-mark" />
        <p className="mono">Fehler</p>
        <h1>{CONTENT.errorPage.error}</h1>
        <div className="error-actions">
          <Button
            solid
            onClick={() => {
              router.invalidate();
              reset();
            }}
          >
            {CONTENT.errorPage.retry}
          </Button>
          <Button href="/">{CONTENT.errorPage.home}</Button>
        </div>
      </div>
    </main>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  staticData: { sitemap: false },
  head: () => ({
    // Each content route sets its own title, description, canonical and social tags.
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1, viewport-fit=cover" },
      { name: "theme-color", content: "#ECECE9" },
      { name: "format-detection", content: "telephone=no" },
      { title: "RN INVEST" },
      { property: "og:site_name", content: "RN INVEST" },
      { property: "og:locale", content: "de_DE" },
    ],
    links: [
      {
        rel: "preload",
        href: archivoFont,
        as: "font",
        type: "font/woff2",
        crossOrigin: "anonymous",
      },
      { rel: "stylesheet", href: appCss },
      { rel: "icon", href: "/favicon.svg", type: "image/svg+xml" },
      { rel: "icon", href: "/favicon-48.png", type: "image/png", sizes: "48x48" },
      { rel: "apple-touch-icon", href: "/apple-touch-icon.png" },
    ],
  }),
  shellComponent: RootShell,
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootShell({ children }: { children: ReactNode }) {
  return (
    <html lang="de">
      <head>
        <HeadContent />
        <noscript>
          <style>{`.reveal-pending{opacity:1!important;transform:none!important}`}</style>
        </noscript>
      </head>
      <body>
        {children}
        <Scripts />
      </body>
    </html>
  );
}

function RootComponent() {
  const { queryClient } = Route.useRouteContext();

  return (
    <QueryClientProvider client={queryClient}>
      {/* Required: nested routes render here. Removing <Outlet /> breaks all child routes. */}
      <Outlet />
    </QueryClientProvider>
  );
}
