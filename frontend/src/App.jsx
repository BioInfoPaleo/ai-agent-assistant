import {useState} from "react";

function App() {
  const [text, setText] = useState("");
  const [output, setOutput] = useState("");

  async function handleClick() {
    const response = await fetch ("http://localhost:8000/summarise", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text }),
    });
    const data = await response.json();
    setOutput(data.summary);
  }
  
  return (
    <div>
      <h1>CSL Assistant</h1>
      <input
      value={text}
      onChange={(e) => setText(e.target.value)}
      placeholder="Type something ..."

    />

    <button onClick={handleClick}>Submit</button>
    <p>Output: {output}</p>
  </div>
  );
}

export default App;
