interface Window {
  loadPyodide: ({ indexURL: str }) => Promise<any>;
  loadPackage: (str) => Promise<any>;
}
