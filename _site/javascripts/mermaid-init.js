document$.subscribe(() => {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: "dark"
  });
  mermaid.run({
    querySelector: ".mermaid"
  });
});
