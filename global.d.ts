interface Window {
  loadPyodide: ({ indexURL: str, stdout }) => Promise<any>;
  loadPackage: (str) => Promise<any>;
}
