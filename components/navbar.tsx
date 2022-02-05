import styles from "./navbar.module.css";

const Navbar = () => {
  return (
    <div className={styles.nav}>
      <ul>
        <a href="/Resume.docx" download>
          RESUME
        </a>
      </ul>
      <ul>
        <a href="/posts/first-post">WRITEUPS</a>
      </ul>
      <ul>
        <a href="https://github.com/misaelaguayo">GITHUB</a>
      </ul>
      <ul>
        <a href="https://tryhackme.com/p/irishyogashirt">TRYHACKME</a>
      </ul>
      <ul>
        <a href="/posts/certifications">CERTIFICATIONS</a>
      </ul>
    </div>
  );
};
export default Navbar;
