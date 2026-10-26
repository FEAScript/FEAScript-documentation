import React from "react";
import clsx from "clsx";
import useIsBrowser from "@docusaurus/useIsBrowser";

// Sun / moon switch, same as feascript.com. The active icon is driven by
// html[data-theme], so it renders correctly before React hydrates.
function ColorModeToggle({ className, value, onChange }) {
  const isBrowser = useIsBrowser();
  return (
    <button
      className={clsx("nav-icon", "theme-toggle", className)}
      type="button"
      onClick={() => onChange(value === "dark" ? "light" : "dark")}
      disabled={!isBrowser}
      title="Toggle colour theme"
      aria-label="Toggle colour theme"
    >
      <svg
        className="icon-moon"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401" />
      </svg>
      <svg
        className="icon-sun"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
      </svg>
    </button>
  );
}

export default React.memo(ColorModeToggle);
