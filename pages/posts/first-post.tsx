import Head from "next/head";
import Link from "next/link";
import { CSSProperties } from "react";
import Layout from "../../components/layout";

const centerStyle: CSSProperties = {
  textAlign: "center",
};

export default function FirstPost() {
  return (
    <Layout home={undefined}>
      <Head>
        <title>Placeholder for now</title>
      </Head>
      <h1 style={centerStyle}>First Post</h1>
      <h2 style={centerStyle}>
        <Link href="/">
          <a>Back to home</a>
        </Link>
      </h2>
    </Layout>
  );
}
