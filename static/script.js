async function send() {
    const msg = document.getElementById("msg").value;

    const res = await fetch("/honeypot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "x-api-key": "ai_honeypot_demo_key"
        },
        body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    document.getElementById("result").textContent =
        JSON.stringify(data, null, 2);
}
