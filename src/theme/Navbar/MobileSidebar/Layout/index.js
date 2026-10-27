import React from "react";
import clsx from "clsx";
import { useNavbarSecondaryMenu } from "@docusaurus/theme-common/internal";
import { ThemeClassNames } from "@docusaurus/theme-common";

// Single-panel mobile menu: the version selector (the only main-menu item shown on
// mobile) above the docs sidebar, instead of the default two sliding panels.
export default function NavbarMobileSidebarLayout({ header, primaryMenu, secondaryMenu }) {
  const { content } = useNavbarSecondaryMenu();
  const hasSidebar = Boolean(content);

  return (
    <div className={clsx(ThemeClassNames.layout.navbar.mobileSidebar.container, "navbar-sidebar")}>
      {header}
      <div className="navbar-sidebar__items">
        <div
          className={clsx(ThemeClassNames.layout.navbar.mobileSidebar.panel, "navbar-sidebar__item menu")}
        >
          {primaryMenu}
          {hasSidebar && secondaryMenu}
        </div>
      </div>
    </div>
  );
}
