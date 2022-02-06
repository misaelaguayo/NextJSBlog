import styles from "./navbar.module.css";
import Link from "next/link";
import { IconContext } from "react-icons";
import { GiHamburgerMenu } from "react-icons/gi";

const Navbar = () => {
  return (
    <div className={styles.nav}>
      <IconContext.Provider
        value={{ color: "#c2c4c7", className: styles.hamburger }}
      >
        <GiHamburgerMenu />
      </IconContext.Provider>
      <ul>
        <Link href="/Resume.docx">RESUME</Link>
      </ul>
      <ul>
        <Link href="/posts/first-post">WRITEUPS</Link>
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
    </div>
  );
};
export default Navbar;
