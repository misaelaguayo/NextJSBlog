import Head from "next/head";
import styles from "./layout.module.css";
import utilStyles from "../styles/utils.module.css";
import Link from "next/link";
import MyImage from "/public/images/profile144.jpg";
import Navbar from "./navbar";
import Github from "./Github";
import LinkedIn from "./LinkedIn";
import TryHackMe from "./TryHackMe";

const name = "Misael Aguayo";
export const siteTitle = "My Site";

export default function Layout({ children, home = false }) {
  return (
    <div className={styles.container}>
      <Head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="description" content="Misael Aguayo's blog" />
        <meta name="og:title" content={siteTitle} />
        <meta name="twitter:card" content="summary_large_image" />
      </Head>
      <Navbar />
      <div className={styles.content}>
        {!home && (
          <div className={styles.backToHome}>
            <Link href="/">
              <a>← Back to home</a>
            </Link>
          </div>
        )}
        <main>{children}</main>
        <header className={styles.header}>
          {home && (
            <>
              <img
                src={MyImage.src}
                alt={name}
                className={utilStyles.borderCircle}
              />
              <div className={styles.social}>
                <Github
                  height="24"
                  width="24"
                  cursor="pointer"
                  onClick={() =>
                    (window.location.href = "https://github.com/misaelaguayo")
                  }
                />
                <LinkedIn
                  height="24"
                  width="24"
                  cursor="pointer"
                  onClick={() =>
                    (window.location.href =
                      "https://www.linkedin.com/in/misael-aguayo-58b22985/")
                  }
                />
                <TryHackMe
                  height="24"
                  width="24"
                  cursor="pointer"
                  onClick={() =>
                    (window.location.href =
                      "https://tryhackme.com/p/irishyogashirt")
                  }
                />
              </div>
              <h1 className={utilStyles.heading2Xl}>{name}</h1>
            </>
          )}
        </header>
        {!home && (
          <div className={styles.backToHome}>
            <Link href="/">
              <a>← Back to home</a>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
