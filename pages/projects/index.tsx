import Layout from "../../components/layout";

import styles from "./projects.module.css";
export default function projects() {
  return (
    <Layout>
      <h1 style={{ textAlign: "center" }}>Projects</h1>
      <div className={styles.projects}>
        <div className={styles.card}>
          <h3>Rust packet visualizer</h3>
          <p>
            Visualize network packets in real time. Uses sdl2 library in rust
            and displays nodes travelling from one host to another
          </p>
        </div>
        <div className={styles.card}>
          <h3>Brd programming language</h3>
          <p>
            A dynamic toy language implemented in python used to learn more
            about AST and token parsing
          </p>
        </div>
        <div className={styles.card}>
          <h3>Haskell markdown previewer</h3>
          <p>
            {" "}
            A way to preview markdown files in a terminal supporting sixels or
            the kitty graphics protocol. Currently working on creatting a neovim
            plugin to support this
          </p>
        </div>
        <div className={styles.card}>
          <h3>PDF text to speech</h3>
          <p>
            {" "}
            A way to convert pdf files to audio files using Java. Utilized
            multithreading to process text while playing audio
          </p>
        </div>
        <div className={styles.card}>
          <h3>Personal blog</h3>
          <p>
            {" "}
            The site you are viewing right now! Built using Next.js and React.
            Automatically published to s3 on push to repo
          </p>
        </div>
      </div>
    </Layout>
  );
}
