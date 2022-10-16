import Head from "next/head";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import markdownStyles from "../../styles/markdown.module.css";
import { useEffect, useState } from "react";

export default function FirstPost() {
  const [markdown, setMarkdown] = useState(null);
  useEffect(async () => {
    const response = await fetch("/markdown/hackpark.md");
    const text = await response.text();
    setMarkdown(text);
  }, []);

  return (
    <div className={markdownStyles.markdownContainer}>
      <ReactMarkdown children={markdown} className={markdownStyles.markdown} />
    </div>
  );
}
