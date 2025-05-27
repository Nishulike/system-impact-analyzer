async function analyze() {
  const id = document.getElementById("cr_id").value;
  const description = document.getElementById("description").value;

  const response = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ 
      change_request_id: id,
      change_text: description 
    })
  });

  if (!response.ok) {
    document.getElementById("result").innerText = `Error: ${response.statusText}`;
    return;
  }

  const data = await response.json();
  document.getElementById("result").innerText = JSON.stringify(data, null, 2);
}
