import styles from "./navbar.module.css";
import Link from "next/link";
import { IconContext } from "react-icons";
import { GiHamburgerMenu } from "react-icons/gi";
import React, { useState } from "react";

const Navbar = () => {
  const [expanded, setExpanded] = useState(true);

  return (
    <div
      className={expanded ? styles.nav : styles.navhidden}
      onClick={() => setExpanded(!expanded)}
    >
      <div style={{ alignSelf: expanded ? "flex-end" : "flex-start" }}>
        <IconContext.Provider
          value={{ color: "#c2c4c7", className: styles.hamburger }}
        >
          <GiHamburgerMenu />
        </IconContext.Provider>
      </div>
      {expanded && (
        <>
          <ul>
            <Link href="/Resume.docx">RESUME</Link>
          </ul>
          <ul>
            <Link href="/posts/first-post">WRITEUPS</Link>
          </ul>
          <ul>
            <Link href="/projects">PROJECTS</Link>
          </ul>
          <ul>
            <Link href="https://github.com/misaelaguayo">GITHUB</Link>
          </ul>
          <ul>
            <Link href="https://tryhackme.com/p/irishyogashirt">TRYHACKME</Link>
          </ul>
          <ul>
            <Link href="/posts/certifications">CERTIFICATIONS</Link>
          </ul>
          <ul>
            <Link href="/repl">REPL</Link>
          </ul>
        </>
      )}
    </div>
  );
};
export default Navbar;
