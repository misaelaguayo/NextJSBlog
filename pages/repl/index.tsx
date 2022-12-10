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
        setOutput(pyodideInstance.runPython(command));
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
        setPyodideInstance(pyodide);
      }
    }
    main();
  }, []);
  return (
    <section className={replStyles.repl}>
      <h2>REPL</h2>
      <form>
        <label>
          {">"}
          <input
            type="text"
            name="name"
            value={command}
            onChange={(event) => {
              setCommand(event.target.value);
            }}
          />
        </label>
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
