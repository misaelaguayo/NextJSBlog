import styles from "./navbar.module.css";
import Link from "next/link";

const Navbar = () => {
  return (
    <div className={styles.nav}>
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
