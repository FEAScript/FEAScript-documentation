import React from "react";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";

function FooterLink({ item }) {
  const className = "footer__link-item";

  return item.href ? (
    <a className={className} href={item.href}>
      {item.label}
    </a>
  ) : (
    <Link className={className} to={item.to}>
      {item.label}
    </Link>
  );
}

export default function Footer() {
  const { siteConfig } = useDocusaurusContext();
  const { links, copyright } = siteConfig.themeConfig.footer;

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer__links">
          <div className="footer__col footer-brand">
            <a className="footer-brand__wordmark" href="https://feascript.com" aria-label="FEAScript website">
              <svg viewBox="14 79 242 242" aria-hidden="true">
                <polygon points="17,254 190,82 253,317" fill="#d4aa00" />
              </svg>
              <span>
                FEAScrip
                <svg className="wm-t" viewBox="0 0 30 115" fill="none" stroke="currentColor" aria-hidden="true">
                  <path strokeWidth="5.9" d="M15 0V100A11.4 11.4 0 0 0 26.4 111.4H29.5" />
                  <path strokeWidth="5.4" d="M0.4 16.9H29.6" />
                </svg>
              </span>
            </a>
            <p className="footer-brand__tagline">
              Finite element simulation in JavaScript, for the browser and Node.js.
            </p>
            <a className="footer-brand__email" href="mailto:info@feascript.com">
              info@feascript.com
            </a>
          </div>
          {links.map((column) => (
            <div className="footer__col" key={column.title}>
              <div className="footer__title">{column.title}</div>
              <ul className="footer__items">
                {column.items.map((item) => (
                  <li key={item.label}>
                    <FooterLink item={item} />
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="footer__bottom">
          <div className="footer__copyright" dangerouslySetInnerHTML={{ __html: copyright }} />
        </div>
      </div>
    </footer>
  );
}
