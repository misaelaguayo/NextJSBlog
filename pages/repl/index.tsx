import { useEffect, useState } from "react";
import replStyles from "../../styles/repl.module.css";

export default function repl() {
  return <Repl />;
}

export function Repl() {
  const [pyodideInstance, setPyodideInstance] = useState(undefined);
  const [command, setCommand] = useState("");
  const [output, setOutput] = useState("");
  function handleCommand(command: string) {
    if (pyodideInstance) {
      try {
        setOutput(
          pyodideInstance.runPython(
            `from brd_package_misaelaguayo import Brd; Brd.run('${command}')`
          )
        );
      } catch (e) {
        console.log(e);
        setOutput("Some kinda python error");
      }
    }
  }
  useEffect(() => {
    async function main() {
      if (window.loadPyodide) {
        let pyodide = await window.loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.20.0/full/",
        });
        await pyodide.loadPackage(
          "https://test-files.pythonhosted.org/packages/7a/22/a138c87326344bf240275943f9c681003549aeec42e4c3efcd72aea25a11/brd_package_misaelaguayo-0.0.3-py3-none-any.whl"
        );
        setPyodideInstance(pyodide);
      }
    }
    main();
  }, []);
  return (
    <section className={replStyles.repl}>
      <h2>REPL</h2>
      <form>
        <textarea
          rows={4}
          cols={50}
          name="name"
          value={command}
          onChange={(event) => {
            setCommand(event.target.value);
          }}
        />
        <br />
        <input
          type="button"
          onClick={() => {
            handleCommand(command);
          }}
          value="Submit"
        />
      </form>
      <p>{output}</p>
    </section>
  );
}
