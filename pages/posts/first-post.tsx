import ReactMarkdown from "react-markdown";
import markdownStyles from "../../styles/markdown.module.css";
import { useEffect, useState } from "react";
import Layout from "../../components/layout";

export default function FirstPost() {
  const [markdown, setMarkdown] = useState(null);
  useEffect(() => {
    async function markdown() {
      const response = await fetch("/markdown/hackpark.md");
      const text = await response.text();
      setMarkdown(text);
    }
    markdown();
  }, []);

  return (
    <Layout>
      <ReactMarkdown className={markdownStyles.markdown}>
        {markdown}
      </ReactMarkdown>
    </Layout>
  );
}
