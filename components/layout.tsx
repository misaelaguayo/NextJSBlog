import Head from "next/head";
import styles from "./layout.module.css";
import utilStyles from "../styles/utils.module.css";
import Link from "next/link";
import MyImage from "/public/images/profile144.jpg";
import Navbar from "./navbar";

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
        <main>{children}</main>
        <header className={styles.header}>
          {home && (
            <>
              <img
                src={MyImage.src}
                alt={name}
                className={utilStyles.borderCircle}
              />
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
