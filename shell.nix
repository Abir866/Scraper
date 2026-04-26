let
  pkgs = import <nixpkgs> { };

in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    python312Packages.selenium
    python312Packages.lxml
    python312Packages.ollama
    python312Packages.langchain
    python312Packages.langchain-ollama
    python312Packages.langchain-openai
    python312Packages.python-dotenv
    python312Packages.langchain-community
    python312Packages.langchain-text-splitters
    python312Packages.pypdf
    python312Packages.openai
    python312Packages.gradio
    python312Packages.weasyprint
    python312Packages.markdown
    python312Packages.httpx
    typst
  ];

  GREETING = "Hello, Nix!";

  shellHook = ''
    echo $GREETING
  '';
}
