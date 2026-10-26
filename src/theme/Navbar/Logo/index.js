import React from "react";
import Link from "@docusaurus/Link";
import useBaseUrl from "@docusaurus/useBaseUrl";

// Same wordmark as feascript.com: gold triangle + "FEAScrip" + the logo-style "t"
export default function NavbarLogo() {
  return (
    <Link to={useBaseUrl("/")} className="navbar__brand" aria-label="FEAScript documentation home">
      <svg className="brand-mark" viewBox="14 79 242 242" aria-hidden="true">
        <polygon points="17,254 190,82 253,317" fill="#d4aa00" />
      </svg>
      <span className="brand-name">
        FEAScrip
        <svg className="wm-t" viewBox="0 0 30 115" fill="none" stroke="currentColor" aria-hidden="true">
          <path strokeWidth="5.9" d="M15 0V100A11.4 11.4 0 0 0 26.4 111.4H29.5" />
          <path strokeWidth="5.4" d="M0.4 16.9H29.6" />
        </svg>
      </span>
      <span className="brand-tag">docs</span>
    </Link>
  );
}
