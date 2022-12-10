import Head from "next/head";
import Navbar from "../components/navbar";
import Layout, { siteTitle } from "../components/layout";
import utilStyles from "../styles/utils.module.css";
import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js";
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  });
  return (
    <>
      <Head>
        <title>{siteTitle}</title>
      </Head>
      <div className={utilStyles.navBarDiv}>
        <Navbar />
        <Layout home>
          <section className={utilStyles.headingMd}>
            <p>
              I am a software engineer interested in information security. Some
              more of my interests include low level networking, reverse
              engineering, and virtual machine languages
            </p>
            <p>
              This blog will be used to document some of the CTFs I participate
              and some of my interests.{" "}
              <a href="https://www.linkedin.com/in/misael-aguayo-58b22985">
                LinkedIn
              </a>
            </p>
          </section>
        </Layout>
      </div>
    </>
  );
}
