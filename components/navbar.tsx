import styles from "./navbar.module.css";
import Link from "next/link";
import React, { useState } from "react";
import Bar from "./Bar";

const Navbar = () => {
  const [expanded, setExpanded] = useState(true);

  return (
    <div className={expanded ? styles.nav : styles.navhidden}>
      <div className={styles.bar} onClick={() => setExpanded(!expanded)}>
        <Bar height={24} width={24} />
      </div>
      {expanded && (
        <>
          <ul>
            <Link href="/Resume.docx">RESUME</Link>
          </ul>
          <ul>
            <Link href="/projects">PROJECTS</Link>
          </ul>
          <ul>
            <Link href="/posts/first-post">WRITEUPS</Link>
          </ul>
          <ul>
            <Link href="/posts/certifications">CERTIFICATIONS</Link>
          </ul>
          {/* Hide this for now until I can get it working
          <ul>
            <Link href="/repl">REPL</Link>
          </ul> */}
        </>
      )}
    </div>
  );
};
export default Navbar;
