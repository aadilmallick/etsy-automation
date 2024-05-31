const btn = document.querySelector("#oauth")!;

btn.addEventListener("click", async () => {
  const response = await fetch("/api/request-oauth-code");
  if (response.ok) {
    const data = await response.json();
    const tokenUrl = data.url;
    if (!tokenUrl) {
      console.error("No token URL found");
      alert("No token URL found");
      return;
    }
    window.location.href = tokenUrl;
  }
});
