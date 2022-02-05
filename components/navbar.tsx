import styles from "./navbar.module.css";

const Navbar = () => {
  return (
    <div className={styles.nav}>
      <ul>RESUME</ul>
      <ul>WRITEUPS</ul>
      <ul>GITHUB</ul>
      <ul>TRYHACKME</ul>
    </div>
  );
};
export default Navbar;
