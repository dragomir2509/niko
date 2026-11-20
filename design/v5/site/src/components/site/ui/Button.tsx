import type { MouseEventHandler, ReactNode } from "react";
import { Arrow } from "./Icons";

type Props = {
  children: ReactNode;
  href?: string;
  solid?: boolean;
  type?: "button" | "submit";
  disabled?: boolean;
  className?: string;
  onClick?: MouseEventHandler<HTMLElement>;
};

export function Button({
  children,
  href,
  solid = false,
  type = "button",
  disabled,
  className = "",
  onClick,
}: Props) {
  const cls = `btn ${solid ? "btn-solid" : ""} ${className}`.trim();
  const content = (
    <>
      <span>{children}</span>
      <Arrow />
    </>
  );
  if (href)
    return (
      <a className={cls} href={href} onClick={onClick}>
        {content}
      </a>
    );
  return (
    <button className={cls} type={type} disabled={disabled} onClick={onClick}>
      {content}
    </button>
  );
}
